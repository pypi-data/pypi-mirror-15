# Copyright 2013 Cloudbase Solutions SRL
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

"""
Unit tests for the Hyper-V utils V2.
"""

import mock

from hyperv.neutron import utils
from hyperv.neutron import utilsv2
from hyperv.tests import base


class TestHyperVUtilsV2(base.BaseTestCase):

    _FAKE_VSWITCH_NAME = "fake_vswitch_name"
    _FAKE_PORT_NAME = "fake_port_name"
    _FAKE_JOB_PATH = 'fake_job_path'
    _FAKE_RET_VAL = 0
    _FAKE_VM_PATH = "fake_vm_path"
    _FAKE_RES_DATA = "fake_res_data"
    _FAKE_RES_PATH = "fake_res_path"
    _FAKE_VSWITCH = "fake_vswitch"
    _FAKE_VLAN_ID = "fake_vlan_id"
    _FAKE_CLASS_NAME = "fake_class_name"
    _FAKE_ELEMENT_NAME = "fake_element_name"
    _FAKE_HYPERV_VM_STATE = 'fake_hyperv_state'

    _FAKE_ACL_ACT = 'fake_acl_action'
    _FAKE_ACL_DIR = 'fake_acl_dir'
    _FAKE_ACL_TYPE = 'fake_acl_type'
    _FAKE_LOCAL_PORT = 'fake_local_port'
    _FAKE_PROTOCOL = 'fake_port_protocol'
    _FAKE_REMOTE_ADDR = '0.0.0.0/0'
    _FAKE_WEIGHT = 'fake_weight'

    _FAKE_BAD_INSTANCE_ID = 'bad_instance_id'
    _FAKE_INSTANCE_ID = (
        r"Microsoft:609CBAAD-BC13-4A65-AADE-AD95861FE394\\55349F56-72AB-4FA3-"
        "B5FE-6A30A511A419\\C\\776E0BA7-94A1-41C8-8F28-951F524251B5\\77A43184-"
        "5444-49BF-ABE0-2210B72ABA73")

    def setUp(self):
        super(TestHyperVUtilsV2, self).setUp()
        self._utils = utilsv2.HyperVUtilsV2()
        self._utils._wmi_conn = mock.MagicMock()

    def test_metric_svc(self):
        expected = self._utils._conn.Msvm_MetricService()[0]
        self.assertEqual(expected, self._utils._metric_svc)

    def test_init_caches(self):
        conn = self._utils._conn
        mock_port = mock.MagicMock(ElementName=mock.sentinel.port_name)
        conn.Msvm_EthernetPortAllocationSettingData.return_value = [
            mock_port]

        mock_sd = mock.MagicMock(InstanceID=self._FAKE_INSTANCE_ID)
        mock_bad_sd = mock.MagicMock(InstanceID=self._FAKE_BAD_INSTANCE_ID)
        conn.Msvm_EthernetSwitchPortVlanSettingData.return_value = [
            mock_bad_sd, mock_sd]
        conn.Msvm_EthernetSwitchPortSecuritySettingData.return_value = [
            mock_bad_sd, mock_sd]

        self._utils.init_caches()

        self.assertEqual({mock.sentinel.port_name: mock_port},
                         self._utils._switch_ports)
        self.assertEqual([mock_sd], list(self._utils._vlan_sds.values()))
        self.assertEqual([mock_sd], list(self._utils._vsid_sds.values()))

    def test_update_cache(self):
        conn = self._utils._conn
        mock_port = mock.MagicMock(ElementName=mock.sentinel.port_name)
        conn.Msvm_EthernetPortAllocationSettingData.return_value = [
            mock_port]

        self._utils.update_cache()

        self.assertEqual({mock.sentinel.port_name: mock_port},
                         self._utils._switch_ports)

    def test_connect_vnic_to_vswitch_found(self):
        self._test_connect_vnic_to_vswitch(True)

    def test_connect_vnic_to_vswitch_not_found(self):
        self._test_connect_vnic_to_vswitch(False)

    def _test_connect_vnic_to_vswitch(self, found):
        self._utils._get_vnic_settings = mock.MagicMock()

        if not found:
            mock_vm = mock.MagicMock()
            self._utils._get_vm_from_res_setting_data = mock.MagicMock(
                return_value=mock_vm)
            self._utils._add_virt_resource = mock.MagicMock()
        else:
            self._utils._modify_virt_resource = mock.MagicMock()

        self._utils._get_vswitch = mock.MagicMock()
        mock_port = self._mock_get_switch_port_alloc(found=found)
        mock_port.HostResource = []

        self._utils.connect_vnic_to_vswitch(self._FAKE_VSWITCH_NAME,
                                            self._FAKE_PORT_NAME)

        if not found:
            self._utils._add_virt_resource.assert_called_with(mock_vm,
                                                              mock_port)
        else:
            self._utils._modify_virt_resource.assert_called_with(mock_port)

    @mock.patch.object(utilsv2.HyperVUtilsV2, '_modify_virt_resource')
    def test_connect_vnic_to_vswitch_already_connected(self, mock_modify_res):
        mock_port = self._mock_get_switch_port_alloc()
        mock_port.HostResource = [mock.sentinel.vswitch_path]

        self._utils.connect_vnic_to_vswitch(mock.sentinel.switch_name,
                                            mock.sentinel.port_name)

        self.assertFalse(mock_modify_res.called)

    def test_add_virt_resource(self):
        self._test_virt_method('AddResourceSettings', 3, '_add_virt_resource',
                               True, self._FAKE_VM_PATH, [self._FAKE_RES_DATA])

    def test_add_virt_feature(self):
        self._test_virt_method('AddFeatureSettings', 3, '_add_virt_feature',
                               True, self._FAKE_VM_PATH, [self._FAKE_RES_DATA])

    def test_modify_virt_resource(self):
        self._test_virt_method('ModifyResourceSettings', 3,
                               '_modify_virt_resource', False,
                               ResourceSettings=[self._FAKE_RES_DATA])

    def test_remove_virt_resource(self):
        self._test_virt_method('RemoveResourceSettings', 2,
                               '_remove_virt_resource', False,
                               ResourceSettings=[self._FAKE_RES_PATH])

    def test_remove_virt_feature(self):
        self._test_virt_method('RemoveFeatureSettings', 2,
                               '_remove_virt_feature', False,
                               FeatureSettings=[self._FAKE_RES_PATH])

    def _test_virt_method(self, vsms_method_name, return_count,
                          utils_method_name, with_mock_vm, *args, **kwargs):
        mock_svc = self._utils._conn.Msvm_VirtualSystemManagementService()[0]
        vsms_method = getattr(mock_svc, vsms_method_name)
        mock_rsd = self._mock_vsms_method(vsms_method, return_count)
        if with_mock_vm:
            mock_vm = mock.MagicMock()
            mock_vm.path_.return_value = self._FAKE_VM_PATH
            getattr(self._utils, utils_method_name)(mock_vm, mock_rsd)
        else:
            getattr(self._utils, utils_method_name)(mock_rsd)

        if args:
            vsms_method.assert_called_once_with(*args)
        else:
            vsms_method.assert_called_once_with(**kwargs)

    def _mock_vsms_method(self, vsms_method, return_count):
        args = None
        if return_count == 3:
            args = (self._FAKE_JOB_PATH, mock.MagicMock(), self._FAKE_RET_VAL)
        else:
            args = (self._FAKE_JOB_PATH, self._FAKE_RET_VAL)

        vsms_method.return_value = args
        mock_res_setting_data = mock.MagicMock()
        mock_res_setting_data.GetText_.return_value = self._FAKE_RES_DATA
        mock_res_setting_data.path_.return_value = self._FAKE_RES_PATH

        self._utils._check_job_status = mock.MagicMock()

        return mock_res_setting_data

    def _mock_get_switch_port_alloc(self, found=True):
        mock_port = mock.MagicMock()
        patched = mock.patch.object(self._utils, '_get_switch_port_allocation',
                                    return_value=(mock_port, found))
        patched.start()
        self.addCleanup(patched.stop)
        return mock_port

    def test_disconnect_switch_port_delete_port(self):
        self._test_disconnect_switch_port(True)

    def test_disconnect_switch_port_modify_port(self):
        self._test_disconnect_switch_port(False)

    def _test_disconnect_switch_port(self, delete_port):
        mock_sw_port = self._mock_get_switch_port_alloc()
        self._utils._switch_ports[self._FAKE_PORT_NAME] = mock_sw_port
        self._utils._vlan_sds[mock_sw_port.InstanceID] = mock.MagicMock()

        if delete_port:
            self._utils._remove_virt_resource = mock.MagicMock()
        else:
            self._utils._modify_virt_resource = mock.MagicMock()

        self._utils.disconnect_switch_port(self._FAKE_PORT_NAME,
                                           True, delete_port)

        if delete_port:
            self._utils._remove_virt_resource.assert_called_with(mock_sw_port)
            self.assertNotIn(self._FAKE_PORT_NAME, self._utils._switch_ports)
            self.assertNotIn(mock_sw_port.InstanceID, self._utils._vlan_sds)
        else:
            self._utils._modify_virt_resource.assert_called_with(mock_sw_port)

    def test_get_vswitch(self):
        self._utils._conn.Msvm_VirtualEthernetSwitch.return_value = [
            self._FAKE_VSWITCH]
        vswitch = self._utils._get_vswitch(self._FAKE_VSWITCH_NAME)

        self.assertEqual(self._FAKE_VSWITCH, vswitch)

    def test_get_vswitch_not_found(self):
        self._utils._conn.Msvm_VirtualEthernetSwitch.return_value = []
        self.assertRaises(utils.HyperVException, self._utils._get_vswitch,
                          self._FAKE_VSWITCH_NAME)

    def test_get_vswitch_external_port(self):
        vswitch = mock.MagicMock(Name=mock.sentinel.vswitch_name)
        self._utils._conn.Msvm_VirtualEthernetSwitch.return_value = [vswitch]

        ext_port = mock.MagicMock()
        lan_endpoint1 = mock.MagicMock()
        ext_port.associators.return_value = [lan_endpoint1]
        lan_endpoint2 = mock.MagicMock(SystemName=mock.sentinel.vswitch_name)
        lan_endpoint1.associators.return_value = [lan_endpoint2]

        self._utils._conn.Msvm_ExternalEthernetPort.return_value = [ext_port]

        result = self._utils._get_vswitch_external_port(mock.sentinel.name)
        self.assertEqual(ext_port, result)

    @mock.patch.object(utilsv2.HyperVUtilsV2, '_get_vswitch_external_port')
    def test_get_vswitch_external_network_name(self, mock_get_vswitch_port):
        mock_get_vswitch_port.return_value.ElementName = (
            mock.sentinel.network_name)
        result = self._utils.get_vswitch_external_network_name(
            mock.sentinel.vswitch_name)
        self.assertEqual(mock.sentinel.network_name, result)

    @mock.patch.object(utilsv2.HyperVUtilsV2, '_get_default_setting_data')
    def test_set_vswitch_port_vlan_id(self, mock_get_default_sd):
        self._mock_get_switch_port_alloc(found=True)

        mock_svc = self._utils._conn.Msvm_VirtualSystemManagementService()[0]
        mock_svc.RemoveFeatureSettings.return_value = (self._FAKE_JOB_PATH,
                                                       self._FAKE_RET_VAL)
        mock_vlan_settings = mock.MagicMock()
        self._utils._get_vlan_setting_data = mock.MagicMock(return_value=(
            mock_vlan_settings, True))

        mock_svc.AddFeatureSettings.return_value = (self._FAKE_JOB_PATH,
                                                    None,
                                                    self._FAKE_RET_VAL)

        self._utils.set_vswitch_port_vlan_id(self._FAKE_VLAN_ID,
                                             self._FAKE_PORT_NAME)

        self.assertTrue(mock_svc.RemoveFeatureSettings.called)
        self.assertTrue(mock_svc.AddFeatureSettings.called)

    @mock.patch.object(utilsv2.HyperVUtilsV2,
                       '_get_vlan_setting_data_from_port_alloc')
    def test_set_vswitch_port_vlan_id_already_set(self, mock_get_vlan_sd):
        self._mock_get_switch_port_alloc()
        mock_get_vlan_sd.return_value = mock.MagicMock(
            AccessVlanId=mock.sentinel.vlan_id,
            OperationMode=self._utils._OPERATION_MODE_ACCESS)

        self._utils.set_vswitch_port_vlan_id(mock.sentinel.vlan_id,
                                             mock.sentinel.port_name)

        mock_svc = self._utils._conn.Msvm_VirtualSystemManagementService()[0]
        self.assertFalse(mock_svc.RemoveFeatureSettings.called)
        self.assertFalse(mock_svc.AddFeatureSettings.called)

    @mock.patch.object(utilsv2.HyperVUtilsV2, '_add_virt_feature')
    @mock.patch.object(utilsv2.HyperVUtilsV2, '_remove_virt_feature')
    @mock.patch.object(utilsv2.HyperVUtilsV2, '_get_default_setting_data')
    def test_set_vswitch_port_vsid(self, mock_get_default_sd, mock_rm_feat,
                                   mock_add_feat):
        mock_port_alloc = self._mock_get_switch_port_alloc()

        mock_vsid_settings = mock.MagicMock()
        mock_port_alloc.associators.return_value = [mock_vsid_settings]
        mock_get_default_sd.return_value = mock_vsid_settings

        self._utils.set_vswitch_port_vsid(mock.sentinel.vsid,
                                          mock.sentinel.switch_port_name)

        mock_rm_feat.assert_called_once_with(mock_vsid_settings)
        mock_add_feat.assert_called_once_with(mock_port_alloc,
                                              mock_vsid_settings)

    @mock.patch.object(utilsv2.HyperVUtilsV2, '_add_virt_feature')
    def test_set_vswitch_port_vsid_already_set(self, mock_add_feat):
        mock_port_alloc = self._mock_get_switch_port_alloc()

        mock_vsid_settings = mock.MagicMock(VirtualSubnetId=mock.sentinel.vsid)
        mock_port_alloc.associators.return_value = (mock_vsid_settings, True)

        self._utils.set_vswitch_port_vsid(mock.sentinel.vsid,
                                          mock.sentinel.switch_port_name)

        self.assertFalse(mock_add_feat.called)

    @mock.patch.object(utilsv2.HyperVUtilsV2,
                       '_get_setting_data_from_port_alloc')
    def test_get_vlan_setting_data_from_port_alloc(self, mock_get_sd):
        mock_port = mock.MagicMock()
        result = self._utils._get_vlan_setting_data_from_port_alloc(mock_port)

        self.assertEqual(mock_get_sd.return_value, result)
        mock_get_sd.assert_called_once_with(mock_port, self._utils._vsid_sds,
                                            self._utils._PORT_VLAN_SET_DATA)

    @mock.patch.object(utilsv2.HyperVUtilsV2,
                       '_get_setting_data_from_port_alloc')
    def test_get_security_setting_data_from_port_alloc(self, mock_get_sd):
        mock_port = mock.MagicMock()
        result = self._utils._get_security_setting_data_from_port_alloc(
            mock_port)

        self.assertEqual(mock_get_sd.return_value, result)
        mock_get_sd.assert_called_once_with(
            mock_port, self._utils._vsid_sds,
            self._utils._PORT_SECURITY_SET_DATA)

    def test_get_setting_data_from_port_alloc_cached(self):
        mock_port = mock.MagicMock(InstanceID=mock.sentinel.InstanceID)
        cache = {mock_port.InstanceID: mock.sentinel.sd_object}

        result = self._utils._get_setting_data_from_port_alloc(
            mock_port, cache, mock.sentinel.data_class)

        self.assertEqual(mock.sentinel.sd_object, result)

    def test_get_setting_data_from_port_alloc(self):
        sd_object = mock.MagicMock()
        mock_port = mock.MagicMock(InstanceID=mock.sentinel.InstanceID)
        mock_port.associators.return_value = [sd_object]
        cache = {}

        result = self._utils._get_setting_data_from_port_alloc(
            mock_port, cache, mock.sentinel.data_class)

        self.assertEqual(sd_object, result)
        self.assertEqual(sd_object, cache[mock.sentinel.InstanceID])

    def test_get_switch_port_allocation_cached(self):
        self._utils._switch_ports[mock.sentinel.port_name] = (
            mock.sentinel.port)

        port, found = self._utils._get_switch_port_allocation(
            mock.sentinel.port_name)

        self.assertEqual(mock.sentinel.port, port)
        self.assertTrue(found)

    @mock.patch.object(utilsv2.HyperVUtilsV2, '_get_setting_data')
    def test_get_switch_port_allocation(self, mock_get_set_data):
        mock_get_set_data.return_value = (mock.sentinel.port, True)

        port, found = self._utils._get_switch_port_allocation(
            mock.sentinel.port_name)

        self.assertEqual(mock.sentinel.port, port)
        self.assertTrue(found)
        self.assertIn(mock.sentinel.port_name, self._utils._switch_ports)
        mock_get_set_data.assert_called_once_with(
            self._utils._PORT_ALLOC_SET_DATA, mock.sentinel.port_name, False)

    def test_get_setting_data(self):
        self._utils._get_first_item = mock.MagicMock(return_value=None)

        mock_data = mock.MagicMock()
        self._utils._get_default_setting_data = mock.MagicMock(
            return_value=mock_data)

        ret_val = self._utils._get_setting_data(self._FAKE_CLASS_NAME,
                                                self._FAKE_ELEMENT_NAME,
                                                True)

        self.assertEqual(ret_val, (mock_data, False))

    def test_create_default_setting_data(self):
        result = self._utils._create_default_setting_data('FakeClass')

        fake_class = self._utils._conn.FakeClass
        self.assertEqual(fake_class.new.return_value, result)
        fake_class.new.assert_called_once_with()

    def test_enable_port_metrics_collection(self):
        mock_port = self._mock_get_switch_port_alloc()
        mock_acl = mock.MagicMock()

        with mock.patch.multiple(
            self._utils,
            _get_default_setting_data=mock.MagicMock(return_value=mock_acl),
            _add_virt_feature=mock.MagicMock()):

            self._utils.enable_port_metrics_collection(self._FAKE_PORT_NAME)

            self.assertEqual(4, len(self._utils._add_virt_feature.mock_calls))
            self._utils._add_virt_feature.assert_called_with(
                mock_port, mock_acl)

    def test_enable_control_metrics_ok(self):
        mock_metrics_svc = self._utils._conn.Msvm_MetricService()[0]
        mock_metrics_def_source = self._utils._conn.CIM_BaseMetricDefinition
        mock_metric_def = mock.MagicMock()
        mock_port = self._mock_get_switch_port_alloc()

        mock_metrics_def_source.return_value = [mock_metric_def]
        m_call = mock.call(Subject=mock_port.path_.return_value,
                           Definition=mock_metric_def.path_.return_value,
                           MetricCollectionEnabled=self._utils._METRIC_ENABLED)

        self._utils.enable_control_metrics(self._FAKE_PORT_NAME)

        mock_metrics_svc.ControlMetrics.assert_has_calls([m_call, m_call])

    def test_enable_control_metrics_no_port(self):
        mock_metrics_svc = self._utils._conn.Msvm_MetricService()[0]
        self._mock_get_switch_port_alloc(found=False)

        self._utils.enable_control_metrics(self._FAKE_PORT_NAME)
        self.assertEqual(0, mock_metrics_svc.ControlMetrics.call_count)

    def test_enable_control_metrics_no_def(self):
        mock_metrics_svc = self._utils._conn.Msvm_MetricService()[0]
        mock_metrics_def_source = self._utils._conn.CIM_BaseMetricDefinition

        self._mock_get_switch_port_alloc()
        mock_metrics_def_source.return_value = None

        self._utils.enable_control_metrics(self._FAKE_PORT_NAME)
        self.assertEqual(0, mock_metrics_svc.ControlMetrics.call_count)

    @mock.patch('hyperv.neutron.utilsv2.HyperVUtilsV2._is_port_vm_started')
    def test_can_enable_control_metrics_true(self, mock_is_started):
        mock_acl = mock.MagicMock()
        mock_acl.Action = self._utils._ACL_ACTION_METER
        self._test_can_enable_control_metrics(mock_is_started,
                                              [mock_acl, mock_acl], True)

    @mock.patch('hyperv.neutron.utilsv2.HyperVUtilsV2._is_port_vm_started')
    def test_can_enable_control_metrics_false(self, mock_is_started):
        self._test_can_enable_control_metrics(mock_is_started, [],
                                              False)

    def _test_can_enable_control_metrics(self, mock_vm_started, acls,
                                         expected_result):
        mock_port = self._mock_get_switch_port_alloc()
        mock_acl = mock.MagicMock()
        mock_acl.Action = self._utils._ACL_ACTION_METER

        mock_port.associators.return_value = acls
        mock_vm_started.return_value = True

        result = self._utils.can_enable_control_metrics(self._FAKE_PORT_NAME)
        self.assertEqual(expected_result, result)

    def test_is_port_vm_started_true(self):
        self._test_is_port_vm_started(self._utils._HYPERV_VM_STATE_ENABLED,
                                      True)

    def test_is_port_vm_started_false(self):
        self._test_is_port_vm_started(self._FAKE_HYPERV_VM_STATE, False)

    def _test_is_port_vm_started(self, vm_state, expected_result):
        mock_svc = self._utils._conn.Msvm_VirtualSystemManagementService()[0]
        mock_port = mock.MagicMock()
        mock_vmsettings = mock.MagicMock()
        mock_summary = mock.MagicMock()
        mock_summary.EnabledState = vm_state
        mock_vmsettings.path_.return_value = self._FAKE_RES_PATH

        mock_port.associators.return_value = [mock_vmsettings]
        mock_svc.GetSummaryInformation.return_value = (self._FAKE_RET_VAL,
                                                       [mock_summary])

        result = self._utils._is_port_vm_started(mock_port)
        self.assertEqual(expected_result, result)
        mock_svc.GetSummaryInformation.assert_called_once_with(
            [self._utils._VM_SUMMARY_ENABLED_STATE],
            [self._FAKE_RES_PATH])

    @mock.patch('hyperv.neutron.utilsv2.HyperVUtilsV2._bind_security_rules')
    def test_create_security_rules(self, mock_bind):
        (m_port, m_acl) = self._setup_security_rule_test()
        fake_rule = mock.MagicMock()

        self._utils.create_security_rules(self._FAKE_PORT_NAME, fake_rule)
        mock_bind.assert_called_once_with(m_port, fake_rule)

    @mock.patch.object(utilsv2.HyperVUtilsV2, '_add_multiple_virt_features')
    @mock.patch('hyperv.neutron.utilsv2.HyperVUtilsV2._create_security_acl')
    @mock.patch('hyperv.neutron.utilsv2.HyperVUtilsV2._get_new_weights')
    @mock.patch('hyperv.neutron.utilsv2.HyperVUtilsV2._filter_security_acls')
    def test_bind_security_rules(self, mock_filtered_acls, mock_get_weights,
                                 mock_create_acl, mock_add):
        m_port = mock.MagicMock()
        m_acl = mock.MagicMock()
        m_port.associators.return_value = [m_acl]
        mock_filtered_acls.return_value = []
        mock_get_weights.return_value = [mock.sentinel.FAKE_WEIGHT]
        mock_create_acl.return_value = m_acl
        fake_rule = mock.MagicMock()

        self._utils._bind_security_rules(m_port, [fake_rule])

        mock_create_acl.assert_called_once_with(fake_rule,
                                                mock.sentinel.FAKE_WEIGHT)
        mock_add.assert_called_once_with(m_port, [m_acl])
        self.assertEqual([m_acl, fake_rule],
                         self._utils._sg_acl_sds[m_port.ElementName])

    @mock.patch('hyperv.neutron.utilsv2.HyperVUtilsV2._get_new_weights')
    @mock.patch('hyperv.neutron.utilsv2.HyperVUtilsV2._filter_security_acls')
    def test_bind_security_rules_existent(self, mock_filtered_acls,
                                          mock_get_weights):
        m_port = mock.MagicMock()
        m_acl = mock.MagicMock()
        m_port.associators.return_value = [m_acl]
        mock_filtered_acls.return_value = [m_acl]
        fake_rule = mock.MagicMock()

        self._utils._bind_security_rules(m_port, [fake_rule])
        mock_filtered_acls.assert_called_once_with(fake_rule, [m_acl])
        mock_get_weights.assert_called_once_with([fake_rule], [m_acl])
        self.assertEqual([m_acl], self._utils._sg_acl_sds[m_port.ElementName])

    def test_get_port_security_acls_cached(self):
        mock_port = mock.MagicMock(ElementName=mock.sentinel.port_name)
        self._utils._sg_acl_sds = {
            mock.sentinel.port_name: [mock.sentinel.fake_acl]}

        acls = self._utils._get_port_security_acls(mock_port)

        self.assertEqual([mock.sentinel.fake_acl], acls)

    def test_get_port_security_acls(self):
        mock_port = mock.MagicMock()
        mock_port.associators.return_value = [mock.sentinel.fake_acl]

        acls = self._utils._get_port_security_acls(mock_port)

        self.assertEqual([mock.sentinel.fake_acl], acls)
        self.assertEqual({mock_port.ElementName: [mock.sentinel.fake_acl]},
                         self._utils._sg_acl_sds)

    @mock.patch.object(utilsv2.HyperVUtilsV2, '_remove_multiple_virt_features')
    @mock.patch.object(utilsv2.HyperVUtilsV2, '_filter_security_acls')
    def test_remove_security_rules(self, mock_filter, mock_remove_feature):
        mock_port, mock_acl = self._setup_security_rule_test()
        mock_port.associators.return_value.append(mock.sentinel.fake_acl)
        fake_rule = mock.MagicMock()
        mock_filter.return_value = [mock_acl]

        self._utils.remove_security_rules(self._FAKE_PORT_NAME, [fake_rule])
        mock_remove_feature.assert_called_once_with([mock_acl])
        self.assertEqual([mock.sentinel.fake_acl],
                         self._utils._sg_acl_sds[mock_port.ElementName])

    @mock.patch.object(utilsv2.HyperVUtilsV2, '_remove_multiple_virt_features')
    def test_remove_all_security_rules(self, mock_remove_feature):
        mock_port, mock_acl = self._setup_security_rule_test()
        self._utils._sg_acl_sds[mock_port.ElementName] = [
            mock.sentinel.fake_acl]

        self._utils.remove_all_security_rules(self._FAKE_PORT_NAME)
        self._utils._remove_multiple_virt_features.assert_called_once_with(
            [mock_acl])
        self.assertEqual([], self._utils._sg_acl_sds[mock_port.ElementName])

    @mock.patch.object(utilsv2.HyperVUtilsV2, '_create_default_setting_data')
    def test_create_security_acl(self, mock_get_set_data):
        mock_acl = mock_get_set_data.return_value
        fake_rule = mock.MagicMock()
        fake_rule.to_dict.return_value = {"Action": self._FAKE_ACL_ACT}

        self._utils._create_security_acl(fake_rule, self._FAKE_WEIGHT)
        mock_acl.set.assert_called_once_with(Action=self._FAKE_ACL_ACT)

    def _setup_security_rule_test(self):
        mock_port = self._mock_get_switch_port_alloc()
        mock_acl = mock.MagicMock()
        mock_port.associators.return_value = [mock_acl]

        self._utils._filter_security_acls = mock.MagicMock(
            return_value=[mock_acl])

        return (mock_port, mock_acl)

    def test_filter_acls(self):
        mock_acl = mock.MagicMock()
        mock_acl.Action = self._FAKE_ACL_ACT
        mock_acl.Applicability = self._utils._ACL_APPLICABILITY_LOCAL
        mock_acl.Direction = self._FAKE_ACL_DIR
        mock_acl.AclType = self._FAKE_ACL_TYPE
        mock_acl.RemoteAddress = self._FAKE_REMOTE_ADDR

        acls = [mock_acl, mock_acl]
        good_acls = self._utils._filter_acls(
            acls, self._FAKE_ACL_ACT, self._FAKE_ACL_DIR,
            self._FAKE_ACL_TYPE, self._FAKE_REMOTE_ADDR)
        bad_acls = self._utils._filter_acls(
            acls, self._FAKE_ACL_ACT, self._FAKE_ACL_DIR, self._FAKE_ACL_TYPE)

        self.assertEqual(acls, good_acls)
        self.assertEqual([], bad_acls)

    def test_get_new_weights_allow(self):
        actual = self._utils._get_new_weights([mock.ANY, mock.ANY], mock.ANY)
        self.assertEqual([0, 0], actual)


class TestHyperVUtilsV2R2(base.BaseTestCase):

    def setUp(self):
        super(TestHyperVUtilsV2R2, self).setUp()
        self._utils = utilsv2.HyperVUtilsV2R2()
        self._utils._wmi_conn = mock.MagicMock()

    @mock.patch.object(utilsv2.HyperVUtilsV2R2, '_get_default_setting_data')
    def test_create_security_acl(self, mock_get_default_setting_data):
        sg_rule = mock.MagicMock()
        sg_rule.to_dict.return_value = {}

        acl = self._utils._create_security_acl(sg_rule, mock.sentinel.weight)

        self.assertEqual(mock.sentinel.weight, acl.Weight)

    def test_get_new_weights_no_acls_deny(self):
        mock_rule = mock.MagicMock(Action=self._utils._ACL_ACTION_DENY)
        actual = self._utils._get_new_weights([mock_rule], [])
        self.assertEqual([1], actual)

    def test_get_new_weights_no_acls_allow(self):
        mock_rule = mock.MagicMock(Action=self._utils._ACL_ACTION_ALLOW)
        actual = self._utils._get_new_weights([mock_rule, mock_rule], [])

        expected = [self._utils._MAX_WEIGHT - 1, self._utils._MAX_WEIGHT - 2]
        self.assertEqual(expected, actual)

    def test_get_new_weights_deny(self):
        mock_rule = mock.MagicMock(Action=self._utils._ACL_ACTION_DENY)
        mockacl1 = mock.MagicMock(Action=self._utils._ACL_ACTION_DENY,
                                  Weight=1)
        mockacl2 = mock.MagicMock(Action=self._utils._ACL_ACTION_DENY,
                                  Weight=3)

        actual = self._utils._get_new_weights([mock_rule, mock_rule],
                                              [mockacl1, mockacl2])

        self.assertEqual([2, 4], actual)

    def test_get_new_weights_allow(self):
        mock_rule = mock.MagicMock(Action=self._utils._ACL_ACTION_ALLOW)
        mockacl = mock.MagicMock(Action=self._utils._ACL_ACTION_ALLOW,
                                 Weight=self._utils._MAX_WEIGHT - 3)

        actual = self._utils._get_new_weights([mock_rule, mock_rule],
                                              [mockacl])

        expected = [self._utils._MAX_WEIGHT - 4, self._utils._MAX_WEIGHT - 5]
        self.assertEqual(expected, actual)

    def test_get_new_weights_search_available(self):
        mock_rule = mock.MagicMock(Action=self._utils._ACL_ACTION_ALLOW)
        mockacl1 = mock.MagicMock(Action=self._utils._ACL_ACTION_ALLOW,
                                  Weight=self._utils._REJECT_ACLS_COUNT + 1)
        mockacl2 = mock.MagicMock(Action=self._utils._ACL_ACTION_ALLOW,
                                  Weight=self._utils._MAX_WEIGHT - 1)

        actual = self._utils._get_new_weights([mock_rule],
                                              [mockacl1, mockacl2])

        self.assertEqual([self._utils._MAX_WEIGHT - 2], actual)
