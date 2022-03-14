from probe.info_extractors.primitives.flow.tcpip_chunk_stats_biflow_info import \
    TCPIPChunkStatsBiFlowInfo
from probe.info_extractors.primitives.packet.tcpip_packet_info import TCPIPPacketInfo
from probe.info_extractors.primitives.flow.tcpip_flow_info import TCPIPFlowInfo
from probe import constants


class TCPIPChunkStatsBiFlowNoackInfo(TCPIPChunkStatsBiFlowInfo):
    which_packet = TCPIPPacketInfo

    def __init__(self, packet_info: TCPIPPacketInfo):
        super().__init__(packet_info)
        self.packets_selection = None

    def _set_packets_selection(self):
        packets_selection = []
        counter = 0

        packet_process_limit = self.num_skipped_packets + self.num_packets_chunk

        for index in range(len(self.packets)):
            if self.num_skipped_packets < counter <= packet_process_limit:
                if self.packets[index].paysize:
                    packets_selection.append(self.packets[index])
                    counter += 1
                continue
            elif counter > packet_process_limit:
                break

            counter += 1

        self.packets_selection = packets_selection

    def to_dict(self) -> dict:
        self._set_packets_selection()
        return self._compute_stats()
