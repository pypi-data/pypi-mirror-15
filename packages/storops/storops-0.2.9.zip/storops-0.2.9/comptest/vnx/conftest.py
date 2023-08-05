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

import pytest

from comptest.vnx import VNXGeneralFixtureManager

__author__ = 'Cedric Zhuang'

log = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def gf(request):
    """ General fixture for most cases

        Details including:
            vnx  - reference to the system.
            pool - A RAID5 pool with 3 disks created on the fly.
            lun  - A LUN created in the pool.
            snap - A snap created upon the LUN.
    :param request:
    :return:
    """
    manager = None

    def fin():
        log.info('tear down general fixture.')
        if manager:
            manager.clean_up()

    request.addfinalizer(fin)

    log.info('setup general fixture.')
    manager = VNXGeneralFixtureManager()

    return manager
