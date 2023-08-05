from spinnman.messages.scp.impl.scp_dpri_set_reinjection_packet_types \
    import SCPDPRISetReinjectionPacketTypesRequest
from spinnman.processes.abstract_multi_connection_process \
    import AbstractMultiConnectionProcess


class SetDPRIPacketTypesProcess(AbstractMultiConnectionProcess):

    def __init__(self, connection_selector):
        AbstractMultiConnectionProcess.__init__(self, connection_selector)

    def set_packet_types(self, packet_types, core_subsets):
        for core_subset in core_subsets.core_subsets:
            for processor_id in core_subset.processor_ids:
                self._send_request(SCPDPRISetReinjectionPacketTypesRequest(
                    core_subset.x, core_subset.y, processor_id, packet_types))
        self._finish()
        self.check_for_error()
