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

from unittest import TestCase

from hamcrest import assert_that, equal_to, has_item, raises, instance_of

from storops.vnx.resource.port import VNXStorageGroupHBAList
from test.vnx.cli_mock import patch_cli, t_cli
from storops.exception import VNXStorageGroupError, \
    VNXStorageGroupNameInUseError, VNXDetachAluNotFoundError, \
    VNXAluAlreadyAttachedError, VNXAluNotFoundError, VNXHluNumberInUseError
from storops.vnx.enums import VNXSPEnum
from storops.vnx.resource.lun import VNXLun
from storops.vnx.resource.sg import VNXStorageGroupList, VNXStorageGroup

__author__ = 'Cedric Zhuang'


class VNXStorageGroupListTest(TestCase):
    @patch_cli()
    def test_get_sg_list(self):
        assert_that(len(VNXStorageGroupList(t_cli())), equal_to(4))


class VNXStorageGroupTest(TestCase):
    def test_sg(self, name='server7'):
        return VNXStorageGroup(name=name, cli=t_cli())

    @patch_cli()
    def test_properties(self):
        sg = self.test_sg()
        assert_that(sg.name, equal_to('server7'))
        assert_that(
            sg.wwn,
            equal_to('F6:F1:04:29:91:97:E5:11:85:E1:AE:04:FD:64:DC:17'))
        assert_that(sg.shareable, equal_to(True))
        assert_that(len(sg.alu_hlu_map), equal_to(2))
        assert_that(sg.alu_hlu_map[10], equal_to(153))
        assert_that(len(sg.hba_sp_pairs), equal_to(15))
        assert_that(sg.uid, equal_to(sg.wwn))
        assert_that(sg.has_alu(10), equal_to(True))
        assert_that(sg.has_alu(11), equal_to(False))
        assert_that(sg.has_hlu(153), equal_to(True))
        assert_that(sg.has_hlu(11), equal_to(False))
        assert_that(sg.existed, equal_to(True))

    @patch_cli()
    def test_get_sg_os01(self):
        sg = VNXStorageGroup(name='os01', cli=t_cli())
        assert_that(len(sg.hba_sp_pairs), equal_to(1))
        assert_that(sg.hba_sp_pairs, instance_of(VNXStorageGroupHBAList))
        hba = sg.hba_sp_pairs[0]
        assert_that(hba.sp, equal_to(VNXSPEnum.SP_A))
        assert_that(hba.uid,
                    equal_to('iqn.1993-08.org.debian:01:95bbe389e025'))
        assert_that(hba.port_id, equal_to(4))

    @patch_cli()
    def test_initiator_uid_list(self):
        sg = self.test_sg('microsoft')
        assert_that(len(sg.initiator_uid_list), equal_to(2))
        assert_that(sg.initiator_uid_list,
                    has_item('iqn.1991-05.com.microsoft:abc.def.dev'))

    @patch_cli()
    def test_hba_ports(self):
        sg = self.test_sg()
        assert_that(len(sg.hba_port_list), equal_to(15))
        assert_that(len(sg.ports), equal_to(8))
        assert_that(len(sg.initiator_uid_list), equal_to(5))

    @patch_cli()
    def test_iscsi_ports_all(self):
        sg = self.test_sg()
        assert_that(len(sg.iscsi_ports), equal_to(1))

    @patch_cli()
    def test_fc_ports_all(self):
        sg = self.test_sg()
        assert_that(len(sg.fc_ports), equal_to(7))

    @patch_cli()
    def test_get_fc_ports_with_filter_found_one(self):
        sg = self.test_sg()
        ports = sg.get_fc_ports(sp=VNXSPEnum.SP_A, port_id=2)
        assert_that(len(ports), equal_to(1))
        port = ports[0]
        assert_that(port.sp, equal_to(VNXSPEnum.SP_A))
        assert_that(port.port_id, equal_to(2))

    @patch_cli()
    def test_get_iscsi_ports_with_filter_type_not_match(self):
        sg = self.test_sg()
        ports = sg.get_iscsi_ports(sp=VNXSPEnum.SP_A, port_id=2)
        assert_that(len(ports), equal_to(0))

    @patch_cli()
    def test_get_port_by_sp(self):
        sg = self.test_sg()
        assert_that(len(sg.get_ports(sp=VNXSPEnum.SP_A)), equal_to(5))
        assert_that(len(sg.get_ports(sp=VNXSPEnum.SP_B)), equal_to(3))
        assert_that(len(sg.get_ports(sp=VNXSPEnum.SP_A, port_id=0)),
                    equal_to(1))
        assert_that(len(sg.get_ports(sp=VNXSPEnum.SP_A, port_id=9)),
                    equal_to(0))

    @patch_cli()
    def test_get_ports_by_wwn(self):
        sg = self.test_sg()
        wwn = '20:00:00:90:FA:53:4C:D0:10:00:00:90:FA:53:4C:D0'
        ports = sg.get_ports(wwn)
        assert_that(len(ports), equal_to(6))
        for port in ports:
            assert_that(port.host_initiator_list, has_item(wwn))

    @patch_cli()
    def test_get_ports_no_wwn(self):
        sg = self.test_sg()
        ports = sg.get_ports()
        assert_that(len(ports), equal_to(8))

    @patch_cli()
    def test_attach_alu_success(self):
        sg = self.test_sg()
        lun = VNXLun(name='x', cli=t_cli())
        assert_that(sg.has_alu(0), equal_to(False))
        hlu = sg.attach_alu(lun)
        assert_that(sg.has_alu(0), equal_to(True))
        assert_that(sg.get_hlu(0), equal_to(1))
        assert_that(hlu, equal_to(1))

    @patch_cli()
    def test_attach_alu_already_attached(self):
        def f():
            sg = self.test_sg()
            sg.attach_alu(123)

        assert_that(f, raises(VNXAluAlreadyAttachedError,
                              'already been added'))

    @patch_cli()
    def test_attach_alu_not_found(self):
        def f():
            sg = self.test_sg()
            sg.attach_alu(124)

        assert_that(f, raises(VNXAluNotFoundError,
                              'not a bound ALU number'))

    @patch_cli()
    def test_attach_alu_hlu_in_use_retry(self):
        def f():
            sg = self.test_sg()
            sg.attach_alu(13, retry_limit=2)

        assert_that(f, raises(VNXHluNumberInUseError,
                              'LUN Number already in use'))

    @patch_cli()
    def test_detach_hlu_success(self):
        sg = self.test_sg()
        sg.detach_alu(10)
        assert_that(sg.has_hlu(10), equal_to(False))

    @patch_cli()
    def test_detach_hlu_not_found(self):
        def f():
            sg = self.test_sg()
            sg.detach_alu(1032)

        assert_that(f, raises(VNXDetachAluNotFoundError, 'No such Host LUN'))

    @patch_cli()
    def test_detach_hlu_not_attached(self):
        def f():
            sg = self.test_sg()
            sg.detach_alu(1033)

        assert_that(f, raises(VNXDetachAluNotFoundError,
                              'is not attached'))

    @patch_cli()
    def test_connect_host(self):
        def f():
            sg = self.test_sg()
            sg.connect_host('host1')

        assert_that(f, raises(VNXStorageGroupError,
                              'Host specified is not known'))

    @patch_cli()
    def test_disconnect_host(self):
        def f():
            sg = self.test_sg()
            sg.disconnect_host('host1')

        assert_that(f, raises(VNXStorageGroupError,
                              'not currently connected'))

    @patch_cli()
    def test_create_sg_name_in_use(self):
        def f():
            VNXStorageGroup.create('existed', t_cli())

        assert_that(f, raises(VNXStorageGroupNameInUseError, 'already in use'))

    @patch_cli()
    def test_empty_sg_property(self):
        sg = VNXStorageGroup.get(t_cli(), 'sg1')
        wwn = 'BB:50:E8:2F:23:01:E6:11:83:36:00:60:16:58:B3:E9'
        assert_that(sg.name, equal_to('sg1'))
        assert_that(sg.wwn, equal_to(wwn))
        assert_that(len(sg.initiator_uid_list), equal_to(0))
        assert_that(len(sg.ports), equal_to(0))
        assert_that(len(sg.fc_ports), equal_to(0))
        assert_that(len(sg.iscsi_ports), equal_to(0))
        assert_that(len(sg.hba_sp_pairs), equal_to(0))
