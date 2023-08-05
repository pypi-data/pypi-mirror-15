from spinnman.messages.scp.impl.scp_dpri_exit_request import SCPDPRIExitRequest
from spinnman.processes.abstract_multi_connection_process \
    import AbstractMultiConnectionProcess


class ExitDPRIProcess(AbstractMultiConnectionProcess):

    def __init__(self, connection_selector):
        AbstractMultiConnectionProcess.__init__(self, connection_selector)

    def exit(self, core_subsets):
        for core_subset in core_subsets.core_subsets:
            for processor_id in core_subset.processor_ids:
                self._send_request(SCPDPRIExitRequest(
                    core_subset.x, core_subset.y, processor_id))
        self._finish()
        self.check_for_error()
