from spinnman.messages.scp.impl.scp_sdram_de_alloc_request import \
    SCPSDRAMDeAllocRequest
from spinnman.processes.abstract_multi_connection_process \
    import AbstractMultiConnectionProcess


class DeAllocSDRAMProcess(AbstractMultiConnectionProcess):

    def __init__(self, connection_selector):
        AbstractMultiConnectionProcess.__init__(self, connection_selector)
        self._no_blocks_freed = None

    def de_alloc_sdram(self, x, y, app_id, base_address=None):

        # deallocate space in the SDRAM
        if base_address is not None:
            self._send_request(
                SCPSDRAMDeAllocRequest(x, y, app_id, base_address))
        else:
            self._send_request(SCPSDRAMDeAllocRequest(x, y, app_id),
                               self.handle_sdram_alloc_response)
        self._finish()
        self.check_for_error()

    def handle_sdram_alloc_response(self, response):
        self._no_blocks_freed = response.number_of_blocks_freed

    @property
    def no_blocks_freed(self):
        return self._no_blocks_freed
