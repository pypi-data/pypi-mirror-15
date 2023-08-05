from spinnman.messages.eieio.eieio_type import EIEIOType
from spinnman.messages.eieio.data_messages.eieio_without_payload_data_message\
    import EIEIOWithoutPayloadDataMessage
from spinnman.messages.eieio.data_messages.eieio_data_header\
    import EIEIODataHeader
from spinnman.messages.eieio.data_messages.eieio_data_message\
    import EIEIODataMessage


class EIEIO32BitPayloadPrefixLowerKeyPrefixDataMessage(
        EIEIOWithoutPayloadDataMessage):
    """ An EIEIO packet containing 32 bit events, a key prefix to be applied\
        to the lower end of the key, and a fixed payload
    """
    def __init__(self, key_prefix, payload_prefix, count=0, data=None,
                 offset=0):
        EIEIOWithoutPayloadDataMessage.__init__(
            self, EIEIODataHeader(EIEIOType.KEY_32_BIT,
                                  payload_prefix=payload_prefix,
                                  prefix=key_prefix, count=count),
            data, offset)

    @staticmethod
    def get_min_packet_length():
        return EIEIODataMessage.min_packet_length(
            EIEIOType.KEY_32_BIT, is_payload_base=True, is_prefix=True)
