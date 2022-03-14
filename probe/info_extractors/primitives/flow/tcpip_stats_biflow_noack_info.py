from probe.info_extractors.primitives.flow.tcpip_stats_biflow_info import TCPIPStatsBiFlowInfo
from probe.info_extractors.primitives.packet.tcpip_packet_info import TCPIPPacketInfo


class TCPIPStatsBiFlowNoackInfo(TCPIPStatsBiFlowInfo):
    which_packet = TCPIPPacketInfo

    def __init__(self, packet_info: TCPIPPacketInfo):
        super().__init__(packet_info)

    def _set_packets_selection(self):
        packets_selection = []

        for index in range(len(self.packets)):
            if not self.packets[index].tcp_flag_ack and not self.packets[index].tcp_flag_syn and \
                    not self.packets[index].tcp_flag_fin and not self.packets[index].tcp_flag_rst:
                packets_selection.append(self.packets[index])

        self.packets_selection = packets_selection

    def to_dict(self) -> dict:
        self._set_packets_selection()
        return self._compute_stats()
