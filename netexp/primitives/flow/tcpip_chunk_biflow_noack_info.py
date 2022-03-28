from netexp.primitives.flow.tcpip_chunk_biflow_info import TCPIPChunkBiFlowInfo
from netexp.primitives.flow.tcpip_chunk_stats_biflow_noack_info import TCPIPChunkStatsBiFlowNoackInfo
from netexp.primitives.packet.tcpip_packet_info import TCPIPPacketInfo


class TCPIPChunkBiFlowNoackInfo(TCPIPChunkBiFlowInfo, TCPIPChunkStatsBiFlowNoackInfo):
    which_packet = TCPIPPacketInfo

    def to_dict(self) -> dict:
        TCPIPChunkStatsBiFlowNoackInfo._set_packets_selection(self)
        return TCPIPChunkBiFlowInfo._extract_stats(self)
