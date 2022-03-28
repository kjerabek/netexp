from netexp.primitives.flow.tcpip_chunk_stats_biflow_info import \
    TCPIPChunkStatsBiFlowInfo
from netexp.primitives.packet.tcpip_packet_info import TCPIPPacketInfo


class TCPIPChunkStatsBiFlowNoackInfo(TCPIPChunkStatsBiFlowInfo):
    which_packet = TCPIPPacketInfo

    def __init__(self, packet_info: TCPIPPacketInfo, config):
        super().__init__(packet_info, config)
        self.packets_selection = None

    def _set_packets_selection(self):
        packets_selection = []
        counter = 0

        packet_process_limit = self.num_skipped_packets + self.num_packets_chunk

        for index in range(len(self.packets)):
            if self.num_skipped_packets <= counter < packet_process_limit:
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
