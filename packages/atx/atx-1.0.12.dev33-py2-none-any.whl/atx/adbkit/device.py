#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import atexit
import os
import re
import json
import collections
import tempfile
from StringIO import StringIO

from PIL import Image
from atx import logutils


logger = logutils.getLogger(__name__)

_DISPLAY_RE = re.compile(
    r'.*DisplayViewport{valid=true, .*orientation=(?P<orientation>\d+), .*deviceWidth=(?P<width>\d+), deviceHeight=(?P<height>\d+).*')
_PROP_PATTERN = re.compile(r'\[(?P<key>.*?)\]:\s*\[(?P<value>.*)\]')


class Device(object):
    Display = collections.namedtuple('Display', ['width', 'height', 'rotation'])
    Package = collections.namedtuple('Package', ['name', 'path'])
    __minicap = '/data/local/tmp/minicap'

    def __init__(self, client, serial):
        self._client = client
        self._serial = serial
        self._screenshot_method = 'minicap'

    @property
    def serial(self):
        return self._serial
    
    def raw_cmd(self, *args):
        args = ['-s', self._serial] + list(args)
        return self._client.raw_cmd(*args)

    def adb_cmd(self, *args):
        """
        Unix style output, already replace \r\n to \n
        """
        p = self.raw_cmd(*args)
        return p.communicate()[0].replace('\r\n', '\n')

    def adb_shell(self, *args):
        """
        Run command `adb shell`
        """
        args = ['shell'] + list(args)
        return self.adb_cmd(*args)

    def keyevent(self, key):
        ''' Call: adb shell input keyevent $key '''
        self.adb_shell('input', 'keyevent', key)

    def remove(self, filename):
        """ 
        Remove file from device
        """
        self.adb_shell('rm', filename)

    def install(self, filename):
        """
        TOOD(ssx): Install apk into device, show progress

        Args:
            - filename(string): apk file path
        """
        return self.adb_cmd('install', '-rt', filename)

    def uninstall(self, package_name, keep_data=False):
        """
        Uninstall package

        Args:
            - package_name(string): package name ex: com.example.demo
            - keep_data(bool): keep the data and cache directories
        """
        if keep_data:
            return self.adb_cmd('uninstall', '-k', package_name)
        else:
            return self.adb_cmd('uninstall', package_name)

    def pull(self, source_file, target_file=None):
        if target_file is None:
            raise RuntimeError('Not supported now')
        self.adb_cmd('pull', source_file, target_file)

    @property
    def display(self):
        '''
        Return device width, height, rotation
        '''
        w, h = (0, 0)
        for line in self.adb_shell('dumpsys', 'display').splitlines():
            m = _DISPLAY_RE.search(line, 0)
            if not m:
                continue
            w = int(m.group('width'))
            h = int(m.group('height'))
            o = int(m.group('orientation'))
            w, h = min(w, h), max(w, h)
            return self.Display(w, h, o)

        output = self.adb_shell('LD_LIBRARY_PATH=/data/local/tmp', self.__minicap, '-i')
        try:
            data = json.loads(output)
            (w, h, o) = (data['width'], data['height'], data['rotation']/90)
            return self.Display(w, h, o)            
        except ValueError:
            pass

    def rotation(self):
        """
        Android rotation
        Return:
            - int [0-4]
        """
        return self.display.rotation
    
    def properties(self):
        '''
        Android Properties, extracted from `adb shell getprop`

        Returns:
            dict of props, for
            example:
                {'ro.bluetooth.dun': 'true'}
        '''
        props = {}
        for line in self.adb_shell(['getprop']).splitlines():
            m = _PROP_PATTERN.match(line)
            if m:
                props[m.group('key')] = m.group('value')
        return props

    def packages(self):
        """
        Show all packages
        """
        pattern = re.compile(r'package:(/[^=]+\.apk)=([^\s]+)')
        packages = []
        for line in self.adb_shell('pm', 'list', 'packages', '-f').splitlines():
            m = pattern.match(line)
            if not m:
                continue
            path, name = m.group(1), m.group(2)
            packages.append(self.Package(name, path))
        return packages

    def _adb_screencap(self, scale=1.0):
        """
        capture screen with adb shell screencap
        """
        remote_file = tempfile.mktemp(dir='/data/local/tmp/', prefix='screencap-', suffix='.png')
        local_file = tempfile.mktemp(prefix='atx-screencap-', suffix='.png')
        self.adb_shell('screencap', '-p', remote_file)
        try:
            self.pull(remote_file, local_file)
            image = Image.open(local_file)
            image.load() # because Image is a lazy load function
            if scale is not None and scale != 1.0:
                image = image.resize([int(scale * s) for s in image.size], Image.BICUBIC)
            rotation = self.rotation()
            if rotation:
                method = getattr(Image, 'ROTATE_{}'.format(rotation*90))
                image = image.transpose(method)
            return image
        finally:
            self.remove(remote_file)
            os.unlink(local_file)

    def _adb_minicap(self, scale=1.0):
        """
        capture screen with minicap

        https://github.com/openstf/minicap
        """
        remote_file = tempfile.mktemp(dir='/data/local/tmp/', prefix='minicap-', suffix='.jpg')
        local_file = tempfile.mktemp(prefix='atx-minicap-', suffix='.jpg')
        (w, h, r) = self.display
        params = '{x}x{y}@{rx}x{ry}/{r}'.format(x=w, y=h, rx=int(w*scale), ry=int(h*scale), r=r*90)
        try:
            self.adb_shell('LD_LIBRARY_PATH=/data/local/tmp', self.__minicap, '-s', '-P', params, '>', remote_file)
            self.pull(remote_file, local_file)
            with open(local_file, 'rb') as f:
                image = Image.open(StringIO(f.read()))
            return image
        finally:
            self.remove(remote_file)
            os.unlink(local_file)

    def screenshot(self, filename=None, scale=1.0, method=None):
        """
        Take device screenshot

        Args:
            - filename(string): optional, save int filename
            - scale(float): scale size
            - method(string): one of minicap,screencap

        Return:
            PIL.Image
        """
        image = None
        method = method or self._screenshot_method
        if method == 'minicap':
            try:
                image = self._adb_minicap(scale)
            except Exception as e:
                logger.warn("use minicap failed, fallback to screencap. error detail: %s", e)
                self._screenshot_method = 'screencap'
                return self.screenshot(filename=filename, scale=scale)
        elif method == 'screencap':
            image = self._adb_screencap(scale)
        else:
            raise RuntimeError("No such method(%s)" % method)

        if filename:
            image.save(filename)
        return image

    def click(self, x, y):
        '''
        same as adb -s ${SERIALNO} shell input tap x y
        FIXME(ssx): not tested on horizontal screen
        '''
        self.adb_shell('input', 'tap', str(x), str(y))

    def forward(self, device_port, local_port=None):
        '''
        adb port forward. return local_port
        TODO: not tested
        '''
        return self._client.forward(self.serial, device_port, local_port)

    def is_locked(self):
        """
        Returns:
            - lock state(bool)
        Raises:
            RuntimeError
        """
        _lockScreenRE = re.compile('mShowingLockscreen=(true|false)')
        m = _lockScreenRE.search(self.adb_shell('dumpsys', 'window', 'policy'))
        if m:
            return (m.group(1) == 'true')
        raise RuntimeError("Couldn't determine screen lock state")

    def is_screen_on(self):
        '''
        Checks if the screen is ON.
        Returns:
            True if the device screen is ON
        Raises:
            RuntimeError
        '''

        _screenOnRE = re.compile('mScreenOnFully=(true|false)')
        m = _screenOnRE.search(self.adb_shell('dumpsys', 'window', 'policy'))
        if m:
            return (m.group(1) == 'true')
        raise RuntimeError("Couldn't determine screen ON state")

    def wake(self):
        """
        Wake up device if device locked
        """
        if not self.is_screen_on():
            self.keyevent('POWER')

    def is_keyboard_shown(self):
        dim = self.adb_shell('dumpsys', 'input_method')
        if dim:
            # FIXME: API >= 15 ?
            return "mInputShown=true" in dim
        return False

    def current_app(self):
        """
        Return: (package_name, activity)
        Raises:
            RuntimeError
        """
        _focusedRE = re.compile('mFocusedApp=.*ActivityRecord{\w+ \w+ (?P<package>.*)/(?P<activity>.*) .*')
        m = _focusedRE.search(self.adb_shell('dumpsys', 'window', 'windows'))
        if m:
            return m.group('package'), m.group('activity')
        raise RuntimeError("Couldn't get focused app")
