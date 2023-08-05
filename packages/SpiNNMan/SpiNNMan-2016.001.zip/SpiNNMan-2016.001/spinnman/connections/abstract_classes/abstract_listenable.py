from six import add_metaclass
from abc import ABCMeta
from abc import abstractmethod


@add_metaclass(ABCMeta)
class AbstractListenable(object):

    @abstractmethod
    def get_receive_method(self):
        """ Get the method that receives for this connection
        """

    @abstractmethod
    def is_ready_to_receive(self, timeout=0):
        """ Determines if there is an SCP packet to be read without blocking

        :param timeout: The time to wait before returning if the connection\
                is not ready
        :type timeout: int
        :return: True if there is an SCP packet to be read
        :rtype: bool
        """
        pass
