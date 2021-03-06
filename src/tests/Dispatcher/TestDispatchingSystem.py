from bin.Devices.Manipulator import EventlessManipulatorManager, Manipulator
from bin.Dispatcher.DataController import DataController, DispatchController
from bin.Devices.Propulsion import EventlessPropulsionManager, Propulsion
from bin.Dispatcher.UDPReceiver import EventlessUDPReceiver
from bin.Dispatcher.Dictionary import *
from bin.Settings import SettingsEntity
from bin.Devices import NullDevice
import unittest
import json


simple_dict = {"a": 1, "b": 2, "c": "cccc"}
system_dict = {
    DeviceClass.PROPULSION: {
        PropulsionKeys.LEFT_WHEEL_SPEED: 100,
        PropulsionKeys.RIGHT_WHEEL_SPEED: 100
    },
    DeviceClass.MANIPULATOR: {
        ManipulatorKeysUC.TURRET: ManipulatorDefaultValues.TURRET
    }
}


class TestController(unittest.TestCase):
    def setUp(self):
        self.address = ("127.0.0.1", 1234)
        self.simple_json = json.dumps(simple_dict)
        self.system_json = json.dumps(system_dict)
        self.propulsion_json = json.dumps(system_dict[DeviceClass.PROPULSION])
        self.propulsion_dict = system_dict[DeviceClass.PROPULSION]
        self.manipulator_json = json.dumps(system_dict[DeviceClass.MANIPULATOR])
        self.manipulator_dict = system_dict[DeviceClass.MANIPULATOR]
        self.invalid_json = '{"supposed_to_be_a_right_json": wrong_json'

    def test_udpreceiver_to_data_controller_communication(self):
        controller = DataController(NullDevice(), NullDevice(), NullDevice())
        recvr = EventlessUDPReceiver(controller=controller)
        recvr.on_read_line(self.address, self.simple_json)
        self.assertEqual(self.simple_json, controller.recent_line_acquired)

    def test_data_handling_to_device(self):
        manager = EventlessPropulsionManager(serial_sett_entity=SettingsEntity(""))
        propulsion = Propulsion(device_manager=manager)
        controller = DataController(propulsion, NullDevice(), NullDevice())
        controller.acquire_new_data(self.system_json)
        self.assertTrue(manager.is_line_sent, "Line not sent")

    def test_expected_line_handling_propulsion(self):
        manager = EventlessPropulsionManager(serial_sett_entity=SettingsEntity(""))
        propulsion = Propulsion(device_manager=manager)
        controller = DataController(propulsion, NullDevice(), NullDevice())
        controller.acquire_new_data(self.system_json)
        propulsion_recvd_dict = json.loads(manager.line_sent)
        self.assertDictEqual(self.propulsion_dict, propulsion_recvd_dict)

    def test_expected_line_handling_manipulator(self):
        manager = EventlessManipulatorManager(serial_sett_entity=SettingsEntity(""))
        manipulator = Manipulator(device_manager=manager)
        controller = DataController(NullDevice(), manipulator, NullDevice())
        controller.acquire_new_data(self.system_json)
        manipulator_recvd_dict = json.loads(manager.line_sent)
        self.assertDictContainsSubset(self.manipulator_dict, manipulator_recvd_dict, "MSG")

    def test_json_parsing_on_failure_of_dgram(self):
        manager = EventlessPropulsionManager(serial_sett_entity=SettingsEntity(""))
        propulsion = Propulsion(device_manager=manager)
        controller = DataController(propulsion, NullDevice(), NullDevice())
        controller.acquire_new_data(self.invalid_json)
        self.assertFalse(propulsion.data)

    def test_dispatch_controller_send_to_propulsion(self):
        manager = EventlessPropulsionManager(serial_sett_entity=SettingsEntity(""))
        propulsion = Propulsion(device_manager=manager)
        controller = DispatchController([propulsion])
        controller.acquire_new_data(self.system_json)
        propulsion_recvd_dict = json.loads(manager.line_sent)
        self.assertDictEqual(self.propulsion_dict, propulsion_recvd_dict)

    def test_dispatch_controller_send_to_manipulator(self):
        manager = EventlessManipulatorManager(serial_sett_entity=SettingsEntity(""))
        manipulator = Manipulator(device_manager=manager)
        controller = DispatchController([manipulator])
        controller.acquire_new_data(self.system_json)
        manipulator_recvd_dict = json.loads(manager.line_sent)
        self.assertDictContainsSubset(self.manipulator_dict, manipulator_recvd_dict, "MSG")

    def test_dispatch_controller_json_parsing_on_failure_of_dgram(self):
        manager = EventlessPropulsionManager(serial_sett_entity=SettingsEntity(""))
        propulsion = Propulsion(device_manager=manager)
        controller = DispatchController([propulsion])
        controller.acquire_new_data(self.invalid_json)
        self.assertFalse(propulsion.data)

    def test_dispatch_controller_send_to_propulsion_and_manipulator(self):
        manipulator_manager = EventlessManipulatorManager(serial_sett_entity=SettingsEntity(""))
        propulsion_manager = EventlessManipulatorManager(serial_sett_entity=SettingsEntity(""))
        propulsion = Propulsion(device_manager=propulsion_manager)
        manipulator = Manipulator(device_manager=manipulator_manager)
        controller = DispatchController([propulsion, manipulator])
        controller.acquire_new_data(self.system_json)
        manipulator_recvd_dict = json.loads(manipulator_manager.line_sent)
        propulsion_recvd_dict = json.loads(propulsion_manager.line_sent)
        self.assertDictContainsSubset(self.manipulator_dict, manipulator_recvd_dict, "MSG")
        self.assertDictEqual(self.propulsion_dict, propulsion_recvd_dict)


if __name__ == "__main__":
    unittest.main()
