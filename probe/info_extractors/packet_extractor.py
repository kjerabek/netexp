from probe.info_extractors.base_extractor import BaseExtractor
from probe.info_extractors.primitives.packet.flow_tcpip_packet_info import FlowTCPIPPacketInfo


class PacketExtractor(BaseExtractor):
    def __init__(self):
        self.flows = {}
        self.processed_packets = []

    def process_packet(self, timestamp, packet):
        packet_info = FlowTCPIPPacketInfo(timestamp, packet)

        if packet_info.has_transport_layer():
            self.__update_flow_identifier(packet_info)
            self.processed_packets.append(packet_info)

    def __update_flow_identifier(self, packet_info: FlowTCPIPPacketInfo):
        if packet_info.proto == 'UDP':
            return

        if packet_info.tcp_flag_syn == 1 and packet_info.tcp_flag_ack == 0:
            self.flows[packet_info.flow_key] = packet_info.flow_timestamp_identifier
        else:
            packet_info.flow_timestamp_identifier = self.flows[packet_info.flow_key]
            packet_info.update_identifier()

    def pop_processed(self):
        processed_packets = [packet for packet in self.processed_packets]
        self.processed_packets.clear()
        return processed_packets

    def pop_rest(self):
        return self.pop_processed()
