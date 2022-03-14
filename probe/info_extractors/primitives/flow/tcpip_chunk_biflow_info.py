from probe.info_extractors.primitives.flow.tcpip_chunk_stats_biflow_info import TCPIPChunkStatsBiFlowInfo
from probe.info_extractors.primitives.packet.tcpip_packet_info import TCPIPPacketInfo
from probe import constants


class TCPIPChunkBiFlowInfo(TCPIPChunkStatsBiFlowInfo):
    which_packet = TCPIPPacketInfo

    def __init__(self, packet_info: TCPIPPacketInfo):
        super().__init__(packet_info)

    def _extract_stats_to_dict(self, feature_name: str, attributes: []) -> dict:
        stats = dict()

        for index in range(0, self.num_packets_chunk):
            key = str(index) + '_' + feature_name
            if index < len(attributes):
                stats[key] = attributes[index]
            else:
                stats[key] = None

        return stats

    def _extract_directions(self, src_ips: []):
        stats = dict()
        directions = []
        src_ip = self.packets[0].src_ip

        for index in range(0, self.num_packets_chunk):
            key = str(index) + '_' + 'direction'

            if index < len(src_ips):
                if src_ip[index] == src_ip:
                    stats[key] = constants.DIRECTION_VALUE_AB
                else:
                    stats[key] = constants.DIRECTION_VALUE_BA

            else:
                stats[key] = None

        return directions

    def _extract_stats(self) -> dict:
        stats = dict()
        stats.update(super().to_dict())

        paysize_attributes = self._get_packets_attribute('paysize')
        directions = self._extract_directions(self._get_packets_attribute('src_ip'))
        psh_attributes = self._get_packets_attribute('tcp_flag_psh')

        mixed_attributes = paysize_attributes * directions
        final_attributes = []

        for index in range(0, len(mixed_attributes)):
            if psh_attributes[index]:
                final_attributes.append(mixed_attributes[index] * 1000)
            else:
                final_attributes.append(mixed_attributes[index])

        return self._extract_stats_to_dict('attr', final_attributes)

    def to_dict(self) -> dict:
        return self._extract_stats()