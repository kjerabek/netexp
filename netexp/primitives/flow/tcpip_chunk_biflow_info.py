from netexp.primitives.flow.tcpip_chunk_stats_biflow_info import TCPIPChunkStatsBiFlowInfo
from netexp.primitives.packet.tcpip_packet_info import TCPIPPacketInfo
from netexp.primitives.flow.tcpip_flow_info import TCPIPFlowInfo
from netexp.common import constants
from netexp.common import naming


class TCPIPChunkBiFlowInfo(TCPIPChunkStatsBiFlowInfo):
    which_packet = TCPIPPacketInfo

    def __init__(self, packet_info: TCPIPPacketInfo, config):
        super().__init__(packet_info, config)

    def _extract_stats_to_dict(self, feature_name: str, attributes: []) -> dict:
        stats = dict()

        for index in range(0, self.num_packets_chunk):
            key = f'{index}_{feature_name}'
            if index < len(attributes):
                stats[key] = attributes[index]
            else:
                stats[key] = None

        return stats

    def _extract_directions(self, src_ips: []):
        directions = []
        src_ip = self.packets[0].src_ip

        for index in range(0, self.num_packets_chunk):
            #if index >= len(src_ips):
            #    break

            if src_ips[index] == src_ip:
                directions.append(constants.DIRECTION_VALUE_AB)
            else:
                directions.append(constants.DIRECTION_VALUE_BA)

        return directions

    def _extract_stats(self) -> dict:
        stats = dict()
        stats.update(TCPIPFlowInfo.to_dict(self))

        paysize_attributes = self._get_packets_attribute(naming.L4_PAYSIZE)
        directions = self._extract_directions(self._get_packets_attribute(naming.SRC_IP))
        psh_attributes = self._get_packets_attribute(naming.TCP_FLAG_PSH)

        mixed_attributes = [a * b for a, b in zip(paysize_attributes, directions)]
        final_attributes = []

        for index in range(0, len(mixed_attributes)):
            if psh_attributes[index]:
                final_attributes.append(mixed_attributes[index] * 1000)
            else:
                final_attributes.append(mixed_attributes[index])

        stats.update(self._extract_stats_to_dict(naming.ATTRIBUTE, final_attributes))

        return stats

    def to_dict(self) -> dict:
        self._set_packets_selection()
        return self._extract_stats()
