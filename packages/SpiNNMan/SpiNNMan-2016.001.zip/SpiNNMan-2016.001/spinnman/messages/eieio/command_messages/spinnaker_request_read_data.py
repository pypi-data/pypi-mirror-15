from spinnman.exceptions import SpinnmanInvalidPacketException, \
    SpinnmanInvalidParameterTypeException
from spinnman.messages.eieio.command_messages.eieio_command_message\
    import EIEIOCommandMessage
from spinnman.messages.eieio.command_messages.eieio_command_header\
    import EIEIOCommandHeader
from spinnman import constants
import struct


class SpinnakerRequestReadData(EIEIOCommandMessage):
    """ Message used in the context of the buffering output mechanism which is\
        sent from the SpiNNaker system to the host computer to signal that\
        some data is available to be read
    """
    def __init__(self, x, y, p, region_id, sequence_no, n_requests,
                 channel, start_address, space_to_be_read):
        if not isinstance(channel, list):
            channel = [channel]

        if not isinstance(region_id, list):
            region_id = [region_id]

        if not isinstance(start_address, list):
            start_address = [start_address]

        if not isinstance(space_to_be_read, list):
            space_to_be_read = [space_to_be_read]

        if len(start_address) != n_requests or \
                len(space_to_be_read) != n_requests or \
                len(channel) != n_requests or \
                len(region_id) != n_requests:
            raise SpinnmanInvalidPacketException(
                "SpinnakerRequestReadData",
                "The format for a SpinnakerRequestReadData packet is "
                "invalid: {0:d} request(s), {1:d} start address(es) "
                "defined, {2:d} space(s) to be read defined, {3:d} region(s) "
                "defined, {4:d} channel(s) defined".format(
                    n_requests, len(start_address), len(space_to_be_read),
                    len(region_id), len(channel)))
        EIEIOCommandMessage.__init__(
            self, EIEIOCommandHeader(
                constants.EIEIO_COMMAND_IDS.SPINNAKER_REQUEST_READ_DATA.value))
        self._header = _SpinnakerRequestReadDataHeader(
            x, y, p, n_requests, sequence_no)
        self._requests = _SpinnakerRequestReadDataRequest(
            channel, region_id, start_address, space_to_be_read)

    @property
    def x(self):
        return self._header.x

    @property
    def y(self):
        return self._header.y

    @property
    def p(self):
        return self._header.p

    @property
    def n_requests(self):
        return self._header.n_requests

    @property
    def sequence_no(self):
        return self._header.sequence_no

    def channel(self, request_id):
        return self._requests.channel(request_id)

    def region_id(self, request_id):
        return self._requests.region_id(request_id)

    def start_address(self, request_id):
        return self._requests.start_address(request_id)

    def space_to_be_read(self, request_id):
        return self._requests.space_to_be_read(request_id)

    @staticmethod
    def get_min_packet_length():
        return 16

    @staticmethod
    def from_bytestring(command_header, data, offset):
        (y, x, processor_and_requests, sequence_no) = \
            struct.unpack_from("<BBBB", data, offset)
        p = (processor_and_requests >> 3) & 0x1F
        n_requests = processor_and_requests & 0x7
        offset += 4
        channel = list()
        region_id = list()
        start_address = list()
        space_to_be_read = list()

        for i in xrange(n_requests):
            if i == 0:
                request_channel, request_region_id, request_start_address, \
                    request_space_to_be_read = struct.unpack_from(
                        "<BBII", data, offset)
                offset += 10
            else:
                request_channel, request_region_id, request_start_address, \
                    request_space_to_be_read = struct.unpack_from(
                        "<xxBBII", data, offset)
                offset += 12
            channel.append(request_channel)
            region_id.append(request_region_id)
            start_address.append(request_start_address)
            space_to_be_read.append(request_space_to_be_read)
        return SpinnakerRequestReadData(
            x, y, p, region_id, sequence_no, n_requests, channel,
            start_address, space_to_be_read)

    @property
    def bytestring(self):
        byte_string = super(SpinnakerRequestReadData, self).bytestring
        byte_string += struct.pack("<BB", self.x, self.y)
        n_requests = self.n_requests
        processor_and_request = (self.p << 3) | n_requests

        for i in xrange(n_requests):
            if i == 0:
                byte_string += struct.pack(
                    "<BBBBII", processor_and_request, self.sequence_no,
                    self.channel(i), self.region_id(i),
                    self.start_address(0), self.space_to_be_read(i))
            else:
                byte_string += struct.pack(
                    "<xxBBII", self.channel(i), self.region_id(i),
                    self.start_address(0), self.space_to_be_read(i))
        return byte_string


class _SpinnakerRequestReadDataHeader(object):
    """ Contains the position of the core in the machine (x, y, p), the number\
        of requests and a sequence number
    """
    def __init__(self, x, y, p, n_requests, sequence_no):
        self._x = x
        self._y = y
        self._p = p
        self._n_requests = n_requests
        self._sequence_no = sequence_no

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def p(self):
        return self._p

    @property
    def sequence_no(self):
        return self._sequence_no

    @property
    def n_requests(self):
        return self._n_requests


class _SpinnakerRequestReadDataRequest(object):
    """ Contains a set of requests which refer to the channels used
    """
    def __init__(self, channel, region_id, start_address, space_to_be_read):
        if not isinstance(channel, list):
            self._channel = [channel]
        else:
            self._channel = channel

        if not isinstance(region_id, list):
            self._region_id = [region_id]
        else:
            self._region_id = region_id

        if not isinstance(start_address, list):
            self._start_address = [start_address]
        else:
            self._start_address = start_address

        if not isinstance(space_to_be_read, list):
            self._space_to_be_read = [space_to_be_read]
        else:
            self._space_to_be_read = space_to_be_read

    def channel(self, request_id):
        if len(self._channel) > request_id:
            return self._channel[request_id]
        else:
            SpinnmanInvalidParameterTypeException(
                "request_id", "integer", "channel request needs to be"
                "comprised between 0 and {0:d}; current value: "
                "{1:d}".format(len(self._channel) - 1, request_id))

    def region_id(self, request_id):
        if len(self._region_id) > request_id:
            return self._region_id[request_id]
        else:
            SpinnmanInvalidParameterTypeException(
                "request_id", "integer", "region id request needs to be"
                "comprised between 0 and {0:d}; current value: "
                "{1:d}".format(len(self._region_id) - 1, request_id))

    def start_address(self, request_id):
        if len(self._start_address) > request_id:
            return self._start_address[request_id]
        else:
            SpinnmanInvalidParameterTypeException(
                "request_id", "integer", "start address request needs to be"
                "comprised between 0 and {0:d}; current value: "
                "{1:d}".format(len(self._start_address) - 1, request_id))

    def space_to_be_read(self, request_id):
        if len(self._space_to_be_read) > request_id:
            return self._space_to_be_read[request_id]
        else:
            SpinnmanInvalidParameterTypeException(
                "request_id", "integer", "space to be read request needs to be"
                "comprised between 0 and {0:d}; current value: "
                "{1:d}".format(len(self._space_to_be_read) - 1, request_id))
