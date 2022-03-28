from netexp.primitives.packet.base_tcpip_packet_info import BaseTCPIPPacketInfo
from netexp.primitives.flow.tcpip_flow_info import TCPIPFlowInfo


class TCPIPFlowBaseExtendedFlowInfo(TCPIPFlowInfo):
    packets_selection = None

    def __init__(self, packet_info: BaseTCPIPPacketInfo, config):
        super().__init__(packet_info, config)
        self.packets_selection = self.packets

    def _get_packets_attribute(self, feature_name: str):
        attributes = []
        for packet in self.packets_selection:
            attributes.append(getattr(packet, feature_name))

        return attributes

    def _get_ab_attributes(self, feature_name: str):
        attributes = []
        src_ip = self.packets[0].src_ip

        for packet in self.packets_selection:
            if packet.src_ip == src_ip:
                attributes.append(getattr(packet, feature_name))

        return attributes

    def _get_ba_attributes(self, feature_name: str):
        attributes = []
        src_ip = self.packets[0].src_ip

        for packet in self.packets_selection:
            if packet.src_ip != src_ip:
                attributes.append(getattr(packet, feature_name))

        return attributes
