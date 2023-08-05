from spinnman.messages.scp.abstract_messages.abstract_scp_request\
    import AbstractSCPRequest
from spinnman.messages.sdp.sdp_header import SDPHeader
from spinnman.messages.sdp.sdp_flag import SDPFlag
from spinnman.messages.scp.scp_request_header import SCPRequestHeader
from spinnman.messages.scp.scp_command import SCPCommand
from spinnman.messages.scp.impl.scp_check_ok_response import SCPCheckOKResponse

_NNP_FORWARD_RETRY = (0x3f << 24) | (0x18 << 16)
_NNP_FLOOD_FILL_START = 6


class SCPFloodFillDataRequest(AbstractSCPRequest):
    """ A request to start a flood fill of data
    """

    def __init__(self, nearest_neighbour_id, block_no, base_address, data,
                 offset=0, length=None):
        """

        :param nearest_neighbour_id: The id of the packet, between 0 and 127
        :type nearest_neighbour_id: int
        :param block_no: Which block this block is, between 0 and 255
        :type block_no: int
        :param base_address: The base address where the data is to be loaded
        :type base_address: int
        :param data: The data to load, between 4 and 256 bytes and the size\
                    must be divisible by 4
        :type data: bytearray
        """
        self._size = length
        self._offset = offset
        self._data_to_write = data
        if length is None:
            self._size = len(data)

        argument_1 = _NNP_FORWARD_RETRY | nearest_neighbour_id
        argument_2 = (block_no << 16) | (((self._size / 4) - 1) << 8)

        super(SCPFloodFillDataRequest, self).__init__(
            SDPHeader(flags=SDPFlag.REPLY_EXPECTED, destination_port=0,
                      destination_cpu=0, destination_chip_x=0,
                      destination_chip_y=0),
            SCPRequestHeader(command=SCPCommand.CMD_FFD),
            argument_1=argument_1, argument_2=argument_2,
            argument_3=base_address, data=None)

    @property
    def bytestring(self):
        datastring = super(SCPFloodFillDataRequest, self).bytestring
        data = self._data_to_write[self._offset:self._offset + self._size]
        return datastring + bytes(data)

    def get_scp_response(self):
        return SCPCheckOKResponse("Flood Fill", "CMD_NNP:NNP_FFS")
