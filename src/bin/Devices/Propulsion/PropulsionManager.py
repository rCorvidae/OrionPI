from bin.Devices import EventlessDeviceManager, NullDeviceManager
from bin.Settings.SettingsEntity import SettingsEntity
from bin.IO.SerialEntity import SerialEntity
from circuits import BaseComponent
from circuits import handler


class EventlessPropulsionManager(EventlessDeviceManager):
    def __init__(self, serial_sett_entity=SettingsEntity("")):
        super(EventlessPropulsionManager, self).__init__(serial_sett_entity)

    def on_read_line(self, *args, **kwargs):
        try:
            line = args[0]
        except IndexError:
            return

        if self.device_model:
            self.device_model.update_data_outcoming(line)


class PropulsionManager(BaseComponent, EventlessPropulsionManager):
    def __init__(self, serial_sett_entity=SettingsEntity("")):
        BaseComponent.__init__(self)
        EventlessDeviceManager.__init__(self, serial_sett_entity)
        self.device = SerialEntity(**self.device_conn).register(self)

    @handler("line_read", channel="propulsion")
    def on_read_line(self, *args, **kwargs):
        EventlessPropulsionManager.on_read_line(self, *args, **kwargs)

    def write_line(self, line, *args, **kwargs):
        self.line_sent = line
        self.device.write_line(self.line_sent)


class NullPropulsionManager(BaseComponent, NullDeviceManager):
    def __init__(self, serial_sett_entity=SettingsEntity("")):
        BaseComponent.__init__(self)
        NullDeviceManager.__init__(self, serial_sett_entity)
