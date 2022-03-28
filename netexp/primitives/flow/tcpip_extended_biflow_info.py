from netexp.primitives.flow.tcpip_base_extended_flow_info import TCPIPFlowBaseExtendedFlowInfo
from netexp.primitives.packet.tcpip_packet_info import TCPIPPacketInfo
from netexp.primitives.flow.tcpip_flow_info import TCPIPFlowInfo
from netexp.common import constants
from netexp.common import naming


class TCPIPFlowExtendedBiFlowInfo(TCPIPFlowBaseExtendedFlowInfo):
    which_packet = TCPIPPacketInfo

    def __init__(self, packet_info: TCPIPPacketInfo, config):
        super().__init__(packet_info, config)

    def _extract_directions(self):
        directions = []
        src_ip = self.packets[0].src_ip

        for packet in self.packets:
            if src_ip == packet.src_ip:
                directions.append(constants.DIRECTION_VALUE_AB)
            else:
                directions.append(constants.DIRECTION_VALUE_BA)

        return directions

    def _extract_stats(self) -> dict:
        stats = dict()
        stats.update(TCPIPFlowInfo.to_dict(self))
        stats[naming.TOTAL_PACKETS] = len(self.packets)

        for attribute_name in [naming.TIMESTAMP, naming.L3_HEADER_LENGTH, naming.L4_HEADER_LENGTH,
                               naming.L4_PAYSIZE, naming.TCP_FLAG_PSH, naming.TCP_FLAG_RST,
                               naming.TCP_FLAG_ACK, naming.TCP_FLAG_FIN, naming.TCP_FLAG_SYN]:
            stats[attribute_name] = self._get_packets_attribute(attribute_name)

        stats[naming.PACKET_DIRECTIONS] = self._extract_directions()

        return stats

    def to_dict(self) -> dict:
        return TCPIPFlowExtendedBiFlowInfo._extract_stats(self)
