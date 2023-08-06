#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# License under MIT


from __future__ import absolute_import

import os
import json
import time

import yaml
import subprocess32 as subprocess
from PIL import Image

from atx import consts
from atx import errors
from atx import patch
from atx import base
from atx import imutils
from atx import strutils
from atx.device import Bounds, Display
from atx import logutils
from atx.device.mixin import DeviceMixin, hook_wrap
from atx import ioskit


__dir__ = os.path.dirname(os.path.abspath(__file__))
log = logutils.getLogger(__name__)

class IOSDevice(DeviceMixin):
    def __init__(self, bundle_id=None, udid=None):
        DeviceMixin.__init__(self)

        self.d = ioskit.Device(udid)
        self.udid = self.d.udid

        self._proc = None
        self._display = None #Display(2208, 1242)
        self._scale = 1
        self._load_ios_info()

        self.screen_rotation = 1 # TODO: auto judge

        if not bundle_id:
            print 'WARNING [ios.py]: bundle_id is not set, only limited functions can be used.'
        else:
            self._init_instruments(bundle_id)

    def _load_ios_info(self):
        model = self.d.info['HardwareModel']
        with open(os.path.join(__dir__, 'ios-models.yml'), 'rb') as f:
            items = yaml.load(f.read())
        for item in items:
            if model == item.get('model'):
                (width, height) = map(int, item.get('pixel').split('x'))
                self._scale = item.get('scale')
                self._display = Display(width*self._scale, height*self._scale)
                break
        if self._display is None:
            raise RuntimeError("TODO: not support your phone for now, You need contact the author.")

    @property
    def display(self):
        return self._display

    @property
    def info(self):
        return self.d.info

    @property
    def rotation(self):
        return self._rotation
    
    def _init_instruments(self, bundle_id):
        self._bootstrap = os.path.join(__dir__, 'bootstrap.sh')
        self._bundle_id = bundle_id
        self._env = {'UDID': self.udid, 'BUNDLE_ID': self._bundle_id}
        # 1. remove pipe
        subprocess.check_output([self._bootstrap, 'reset'], env=self._env)
        # 2. start instruments
        self._proc = subprocess.Popen([self._bootstrap, 'instruments'], env=self._env, stdout=subprocess.PIPE)

    def _runjs(self, code):
        # print code
        output = subprocess.check_output([self._bootstrap, 'run', code], env=self._env)
        # print output
        return output
        return json.loads(output)

    def _close(self):
        print 'Terminate instruments'
        if self._proc:
            self._proc.terminate()
        # 1. remove pipe
        subprocess.check_output([self._bootstrap, 'reset'], env=self._env)

    def __del__(self):
        if hasattr(self, '_bootstrap'):
            self._close()

    def screenshot(self, filename=None):
        '''
        Take ios screenshot
        Args:
            - filename(string): optional
        Returns:
            PIL.Image object
        '''
        image = self.d.screenshot()
        if self.screen_rotation:
            method = getattr(Image, 'ROTATE_{}'.format(self.screen_rotation*90))
            image = image.transpose(method)
        if filename:
            image.save(filename)
        return image

    def click(self, x, y):
        self._runjs('target.tap({x: %d, y: %d})' % (x/self._scale, y/self._scale))

    def install(self, filepath):
        raise NotImplementedError()

    def sleep(self, sec):
        time.sleep(sec)

    def type(self, text):
        self._runjs('$.typeString(%s)' % json.dumps(text))

    def current_app(self):
        ''' todo, maybe return dict is a better way '''
        return self._runjs('target.frontMostApp().bundleID()').strip().strip('"')
