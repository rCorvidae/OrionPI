from bin.Utility import LineProcessing


class LineReaderAbstract(LineProcessing):
    def __init__(self, terminator="\r\n", encoding="utf-8"):
        super(LineReaderAbstract, self).__init__(terminator, encoding)
        self._buffer = bytearray()

    def append_data(self, byte_data):
        raise NotImplemented("append_data in LineReaderAbstract not implemented yet")

    def read_line(self):
        raise NotImplemented("read_line in LineReaderAbstract not implemented yet")

    def clear(self):
        raise NotImplemented("clear in LineReaderAbstract not implemented yet")


class LineReader(LineReaderAbstract):
    def __init__(self, terminator="\r\n", encoding="utf-8"):
        super(LineReader, self).__init__(terminator, encoding)

    def append_data(self, byte_data):
        self._buffer.extend(byte_data)

    def read_line(self):
        """Reads a line from buffer. Any remaining data is queued.
        Returns string."""
        line, sep, self._buffer = self._buffer.partition(self.TERMINATOR)

        if not (sep or self._buffer):
            self._buffer = line
            return self.write_line(b"")

        return self.write_line(line)

    def write_line(self, line_of_data):
        """Converts a set of bytes into string based on
        encoding info entered at init."""
        return line_of_data.decode(self.ENCODING)

    def clear(self):
        self._buffer.clear()
