from six import add_metaclass
from abc import ABCMeta
from abc import abstractmethod


@add_metaclass(ABCMeta)
class AbstractEIEIODataElement(object):
    """ A marker interface for possible data elements in the EIEIO data packet
    """

    @abstractmethod
    def get_bytestring(self, eieio_type):
        """ Get a bytestring for the given type

        :param eieio_type: The type of the message being written
        :type eieio_type:\
                    :py:class:`spinnman.messages.eieio.eieio_type.EIEIOType`
        :return: A bytestring for the element
        :rtype: bytestring
        :raise SpinnmanInvalidParameterException: If the type is incompatible\
                    with the element
        """
