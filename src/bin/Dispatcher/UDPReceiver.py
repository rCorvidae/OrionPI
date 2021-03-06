from bin.Settings.SettingsEntity import SettingsEntity
from circuits import BaseComponent, handler
from bin.Dispatcher.DataController import *
from bin.IO.UDPEntity import UDPEntity
from bin.IO import IOStream
from bin.Devices.DeviceObserver import DeviceObserverInterface


class EventlessUDPReceiver(IOStream, DeviceObserverInterface):
    def __init__(self, controller=ControllerAbstract(), udp_sett_entity=SettingsEntity(""), **kwargs):
        self._controller = controller
        self.recent_caller_address = tuple()

    def on_read_line(self, *args, **kwargs):
        try:
            address = args[0]
            msg = args[1]
        except IndexError:
            return
        self.recent_caller_address = address
        self._controller.acquire_new_data(msg)

    def write_line(self, line, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        self.write_line(*args, **kwargs)


class UDPReceiver(BaseComponent, EventlessUDPReceiver):
    def __init__(self, controller=ControllerAbstract(), udp_sett_entity=SettingsEntity(""), **kwargs):
        BaseComponent.__init__(self)
        EventlessUDPReceiver.__init__(self, controller, udp_sett_entity, **kwargs)
        self.udp_conn = udp_sett_entity.get_settings()
        self.udp = UDPEntity(**self.udp_conn).register(self)

    @handler("line_read", channel="UDPServer")
    def on_read_line(self, *args, **kwargs):
        EventlessUDPReceiver.on_read_line(self, *args, **kwargs)

    def write_line(self, line, *args, **kwargs):
        self.udp.write_line(line, *args, **kwargs)
