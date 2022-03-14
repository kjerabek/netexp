from probe.info_extractors.primitives.flow.tcpip_base_extended_flow_info import TCPIPFlowBaseExtendedFlowInfo
from probe.info_extractors.primitives.packet.tcpip_packet_info import TCPIPPacketInfo
from probe.info_extractors.primitives.flow.tcpip_flow_info import TCPIPFlowInfo
from probe import constants


class TCPIPFlowExtendedBiFlowInfo(TCPIPFlowBaseExtendedFlowInfo):
    which_packet = TCPIPPacketInfo

    def __init__(self, packet_info: TCPIPPacketInfo):
        super().__init__(packet_info)

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
        stats['packets'] = len(self.packets)

        for attribute_name in ['timestamp', 'ip_header_len', 'trans_header_len',
                               'paysize', 'tcp_flag_psh', 'tcp_flag_rst', 'tcp_flag_ack',
                               'tcp_flag_fin', 'tcp_flag_syn']:
            stats[attribute_name] = self._get_packets_attribute(attribute_name)

        stats['directions'] = self._extract_directions()

        return stats

    def to_dict(self) -> dict:
        return TCPIPFlowExtendedBiFlowInfo._extract_stats(self)
