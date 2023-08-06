# coding=utf-8
# Copyright (c) 2015 EMC Corporation.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
from __future__ import unicode_literals

import logging
import threading
from logging.handlers import RotatingFileHandler
import sys
import os
from os.path import join, dirname, abspath

import errno
from time import sleep

from retryz import retry

from test.utils import PersistedDict

__author__ = 'Cedric Zhuang'

log = logging.getLogger(__name__)


def log_folder():
    folder = join(dirname(abspath(__file__)), '..', 'logs')
    if not os.path.exists(folder):
        try:
            os.makedirs(folder)
        except OSError as ex:
            if ex.errno != errno.EEXIST:
                raise
    return folder


def setup_log():
    fmt_str = ('%(asctime)s [%(levelname)s] %(process)d '
               '%(name)s - %(message)s')
    level = logging.DEBUG
    filename = join(log_folder(), 'comp_test.log')

    root = logging.getLogger()
    root.setLevel(level)

    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(logging.Formatter(fmt_str))
    ch.setLevel(logging.INFO)

    fh = RotatingFileHandler(filename, maxBytes=10 * 1024 ** 2, backupCount=20)
    fh.setFormatter(logging.Formatter(fmt_str))

    root.addHandler(ch)
    root.addHandler(fh)


class ResourceManager(object):
    def __init__(self, name):
        self._names = self._init_names()
        self._name = name
        self._add_worker()

    def clean_up(self):
        log.info('wait for all workers to exit.')
        while self._remove_worker():
            # wait for all test cases to complete
            sleep(1)

        log.info('start fixture {} clean up.'.format(self.clz_name))

    def _init_names(self):
        data_file = '{}_names'.format(self.clz_name)
        return PersistedDict(data_file, list)

    @property
    def clz_name(self):
        return self.__class__.__name__

    def _add_worker(self):
        workers = self._names['worker']
        _id = threading.current_thread().ident
        if _id not in workers:
            workers.append(_id)
        self._names['worker'] = workers

    def _remove_worker(self):
        workers = self._names['worker']
        _id = threading.current_thread().ident
        if _id in workers:
            workers.remove(_id)
        self._names['worker'] = workers
        return len(workers)

    def has_name(self, rsc_type, key=None):
        names = self._names[rsc_type]
        if names:
            if key is None:
                ret = True
            else:
                ret = key in names
        else:
            ret = False
        return ret

    def _pop_name(self, rsc_type):
        names = self._names[rsc_type]
        ret = names.pop()
        self._names[rsc_type] = names
        return ret

    def add_name(self, rsc_type, name=None):
        names = self._names[rsc_type]
        n = len(names)

        if name is None:
            name = '{}_{}_{}'.format(self._name, rsc_type, n)
        names.append(name)
        self._names[rsc_type] = names
        return name

    @staticmethod
    @retry(on_error=ValueError, wait=5, limit=20)
    def until(obj, checker):
        obj.update()
        if not checker(obj):
            raise ValueError

    @classmethod
    def until_existed(cls, obj):
        return cls.until(obj, lambda x: x.existed)

    @classmethod
    def until_not_existed(cls, obj):
        return cls.until(obj, lambda x: not x.existed)

    ######################
    # has_xxx_name methods
    def has_snap_name(self, name=None):
        return self.has_name('snap', name)

    def has_lun_name(self, name=None):
        return self.has_name('lun', name)

    def has_pool_name(self, name=None):
        return self.has_name('pool', name)

    def has_fs_name(self, name=None):
        return self.has_name('fs', name)

    def has_cg_name(self, name=None):
        return self.has_name('cg', name)

    def has_nas_server_name(self, name=None):
        return self.has_name('nas_server', name)

    def has_cifs_share_name(self, name=None):
        return self.has_name('cifs_share', name)

    def has_nfs_share_name(self, name=None):
        return self.has_name('nfs_share', name)

    def has_sg_name(self, name=None):
        return self.has_name('sg', name)

    ######################
    # add_xxx_name methods
    def add_snap_name(self, name=None):
        return self.add_name('snap', name)

    def add_lun_name(self, name=None):
        return self.add_name('lun', name)

    def add_pool_name(self, name=None):
        return self.add_name('pool', name)

    def add_fs_name(self, name=None):
        return self.add_name('fs', name)

    def add_nas_server_name(self, name=None):
        return self.add_name('nas_server', name)

    def add_cifs_share_name(self, name=None):
        return self.add_name('cifs_share', name)

    def add_nfs_share_name(self, name=None):
        return self.add_name('nfs_share', name)

    def add_sg_name(self, name=None):
        return self.add_name('sg', name)

    def add_cg_name(self, name=None):
        return self.add_name('cg', name)
