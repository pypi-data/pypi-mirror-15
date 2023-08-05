from spinnman.messages.scp.abstract_messages.abstract_scp_request\
    import AbstractSCPRequest
from spinnman.messages.sdp.sdp_header import SDPHeader
from spinnman.messages.sdp.sdp_flag import SDPFlag
from spinnman.messages.scp.scp_request_header import SCPRequestHeader
from spinnman.messages.scp.scp_command import SCPCommand
from spinnman.messages.scp.impl.scp_check_ok_response import SCPCheckOKResponse
from spinnman import constants


class SCPWriteMemoryRequest(AbstractSCPRequest):
    """ A request to write memory on a chip
    """

    def __init__(self, x, y, base_address, data, cpu=0):
        """

        :param x: The x-coordinate of the chip, between 0 and 255\
        this is not checked due to speed restrictions
        :type x: int
        :param y: The y-coordinate of the chip, between 0 and 255\
        this is not checked due to speed restrictions
        :type y: int
        :param base_address: The base_address to start writing to \
        the base address is not checked to see if its not valid
        :type base_address: int
        :param data: between 1 and 256 bytes of data to write\
        this is not checked due to speed restrictions
        :type data: bytearray or string
        """
        size = len(data)
        super(SCPWriteMemoryRequest, self).__init__(
            SDPHeader(
                flags=SDPFlag.REPLY_EXPECTED, destination_port=0,
                destination_cpu=cpu, destination_chip_x=x,
                destination_chip_y=y),
            SCPRequestHeader(command=SCPCommand.CMD_WRITE),
            argument_1=base_address, argument_2=size,
            argument_3=constants.address_length_dtype[
                (base_address % 4), (size % 4)].value,
            data=None)
        self._data_to_write = data

    @property
    def bytestring(self):
        datastring = super(SCPWriteMemoryRequest, self).bytestring
        return datastring + bytes(self._data_to_write)

    def get_scp_response(self):
        return SCPCheckOKResponse("WriteMemory", "CMD_WRITE")
