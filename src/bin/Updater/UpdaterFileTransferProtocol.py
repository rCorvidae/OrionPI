from bin.Updater.UpdaterDataProcessor import UpdaterDataProcessorInterface
from bin.Updater.UpdaterDataAssembly import DataAssemblyInterface
from bin.Updater.UpdaterTransmissionNegotiation import *
from bin.Utility.LineWriter import LineWriter
from bin.Utility.LineReader import LineReader


alias_TN = TransmissionNegotiation


class FileTransferProtocolInterface:
    def run(self, data):
        raise NotImplemented()


class FileTransferProtocol(FileTransferProtocolInterface):
    MSG_DATA_RECVD = "Data received!"
    MSG_TOO_MUCH_DATA = "To much data. Retry!"
    MSG_COULD_NOT_ENCODE = "Could not encode ack!"

    class MODE:
        NEGOTIATE = 0
        GET_DATA = 1

    def __init__(self, negotiator=TransmissionNegotiationInterface(),
                 data_assembly=DataAssemblyInterface(),
                 data_processor=UpdaterDataProcessorInterface(),
                 terminator="\r\n", encoding="utf-8",
                 stdio=lambda io: io, stderr=lambda cerr: cerr):
        self._line_reader = LineReader(terminator, encoding)
        self._line_writer = LineWriter(terminator, encoding)
        self.negotiator = negotiator
        self.data_assembly = data_assembly
        self.mode = self.MODE.NEGOTIATE
        self.stdio = stdio
        self.stderr = stderr
        self.ack = None
        self.data_processor = data_processor

    def is_current_mode(self, mode):
        return self.mode == mode

    def set_current_mode(self, mode):
        self.mode = mode

    def run(self, data):
        if self.is_current_mode(self.MODE.NEGOTIATE):
            self.negotiate(data)
        elif self.is_current_mode(self.MODE.GET_DATA):
            self.assemble_data(data)

    def negotiate(self, data):
        line = self._parse_negotiation_data(data)
        if not line:
            return

        self.ack = self.negotiator.negotiate(line)
        if self.ack:
            self._init_assembly_params()
            self.set_current_mode(self.MODE.GET_DATA)
            self._handle_acknowledgement()

    def assemble_data(self, raw_data):
        self.data_assembly.append_bytes(raw_data)
        if self.data_assembly.can_read():
            self._send_info(self.MSG_DATA_RECVD)
            self._process_recvd_data()
        elif self._has_more_bytes_than_it_should():
            self._handle_error(self.MSG_TOO_MUCH_DATA)

    def _parse_negotiation_data(self, data):
        self._line_reader.append_data(data)
        return self._line_reader.read_line()

    def _init_assembly_params(self):
        bytesize = self.ack.results(alias_TN.ACK, alias_TN.FILE_SIZE)
        md5sum = self.ack.results(alias_TN.ACK, alias_TN.MD5)
        self.data_assembly.init_assembly_params(bytesize, md5sum)

    def _handle_acknowledgement(self):
        ack = self.ack.results()
        try:
            ack = ack if isinstance(ack, str) else json.dumps(ack)
        except json.JSONDecodeError:
            self._handle_error(self.MSG_COULD_NOT_ENCODE)
            return

        self.stdio(ack)

    def _send_info(self, text):
        info_json = self.negotiator.create_msg_to_host(text)
        self.stdio(info_json)

    def _process_recvd_data(self):
        raw_data = self.data_assembly.read_data()
        self.data_processor.process(raw_data)
        filename = self.ack.results(alias_TN.ACK, alias_TN.FILE_NAME)
        self.data_processor.save(filename)
        self._reinit()

    def _has_more_bytes_than_it_should(self):
        return self.data_assembly.bytes_size()\
               > self.ack.results(alias_TN.ACK, alias_TN.FILE_SIZE)

    def _handle_error(self, error_text):
        error_json = self.negotiator.create_msg_to_host(error_text)
        self.stderr(error_json)
        self._reinit()

    def _reinit(self):
        self._line_reader.clear()
        self.data_assembly.clear()
        self.set_current_mode(self.MODE.NEGOTIATE)
        self.ack = None
