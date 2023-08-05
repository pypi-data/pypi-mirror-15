from abc import ABCMeta
from abc import abstractmethod
from six import add_metaclass

from spinnman.connections.abstract_classes.abstract_connection \
    import AbstractConnection


@add_metaclass(ABCMeta)
class AbstractMulticastReceiver(AbstractConnection):
    """ A receiver of Multicast messages
    """

    @abstractmethod
    def get_input_chips(self):
        """ Get a list of chips which identify the chips from which this\
            receiver can receive receive packets directly

        :return: An iterable of tuples of (x, y) where x is the x-coordinate\
                    of the chip and y is the y-coordinate of the chip
        :rtype: iterable of (int, int)
        :raise None: No known exceptions are raised
        """
        pass

    @abstractmethod
    def receive_multicast_message(self, timeout=None):
        """ Receives a multicast message from this connection.  Blocks\
            until a message has been received, or a timeout occurs.

        :param timeout: The time in seconds to wait for the message to arrive;\
                    if not specified, will wait forever, or until the\
                    connection is closed
        :type timeout: int
        :return: a multicast message
        :rtype:\
                    :py:class:`spinnman.messages.multicast_message.MulticastMessage`
        :raise spinnman.exceptions.SpinnmanIOException: If there is an error\
                    receiving the message
        :raise spinnman.exceptions.SpinnmanTimeoutException: If there is a\
                    timeout before a message is received
        :raise spinnman.exceptions.SpinnmanInvalidPacketException: If the\
                    received packet is not a valid multicast message
        :raise spinnman.exceptions.SpinnmanInvalidParameterException: If one\
                    of the fields of the multicast message is invalid
        """
        pass
