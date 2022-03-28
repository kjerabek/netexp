from netexp.primitives.flow.tcpip_stats_biflow_info import TCPIPStatsBiFlowInfo
from netexp.primitives.packet.tcpip_packet_info import TCPIPPacketInfo

from netexp.common import naming


class TCPIPStatsUniBiFlowInfo(TCPIPStatsBiFlowInfo):
    which_packet = TCPIPPacketInfo

    def __init__(self, packet_info: TCPIPPacketInfo, config):
        super().__init__(packet_info, config)

    def _get_abba_push_flag_paysize(self, ab: bool = True) -> list:
        attributes = []
        src_ip = self.packets[0].src_ip

        for packet in self.packets:
            if ab and packet.src_ip == src_ip and packet.tcp_flag_psh:
                attributes.append(packet.paysize)
            if not ab and packet.src_ip != src_ip and packet.tcp_flag_psh:
                attributes.append(packet.paysize)

        return attributes

    @staticmethod
    def _bidirectional_time_stats_to_unidirectional(suffix, stats):
        tmp_stats = dict()

        for key in [naming.MEAN_INTER_ARRIVAL_TIME, naming.STD_INTER_ARRIVAL_TIME, naming.VAR_INTER_ARRIVAL_TIME,
                    naming.MIN_INTER_ARRIVAL_TIME, naming.QUARTILE1_INTER_ARRIVAL_TIME, naming.MED_INTER_ARRIVAL_TIME,
                    naming.QUARTILE3_INTER_ARRIVAL_TIME, naming.MAX_INTER_ARRIVAL_TIME]:
            tmp_stats[key + suffix] = stats[key]

        return tmp_stats

    def _compute_pure_acks_abba(self, ab: bool = True) -> dict:
        stats = dict()
        ack_counter = 0

        for packet in self.packets_selection:
            if packet.tcp_flag_ack and packet.paysize == 0 and not packet.tcp_flag_fin and \
                    not packet.tcp_flag_rst and not packet.tcp_flag_syn:
                if ab and self.packets[0].src_ip == packet.src_ip:
                    ack_counter += 1
                if not ab and self.packets[0].dst_ip == packet.src_ip:
                    ack_counter += 1

        suffix = naming.SUFFIX_AB if ab else naming.SUFFIX_BA
        stats[naming.PURE_ACKS_SENT + suffix] = ack_counter

        return stats

    def _compute_unidirectional_stats(self, ab: bool = True):
        stats = dict()

        if ab:
            suffix = naming.SUFFIX_AB
            direction_attribute_method = self._get_ab_attributes
        else:
            suffix = naming.SUFFIX_BA
            direction_attribute_method = self._get_ba_attributes

        stats[naming.TOTAL_PACKETS + suffix] = len(direction_attribute_method(naming.L4_PAYSIZE))

        for attribute_name in [naming.L3_HEADER_LENGTH, naming.L4_HEADER_LENGTH, naming.L4_PAYSIZE]:
            stats.update(self._compute_all_stats(attribute_name + suffix,
                                                 direction_attribute_method(attribute_name)))

        stats.update(self._compute_no_payload(direction_attribute_method(naming.L4_PAYSIZE), suffix=suffix))

        for attribute_name in [naming.TCP_FLAG_PSH, naming.TCP_FLAG_URG, naming.TCP_FLAG_RST,
                               naming.TCP_FLAG_ACK, naming.TCP_FLAG_FIN, naming.TCP_FLAG_SYN]:
            stats.update(self._compute_sums(attribute_name + suffix,
                                            direction_attribute_method(attribute_name)))

        stats.update(self._compute_all_stats(naming.PSH_PACKETS_L4_PAYSIZE + suffix,
                                             self._get_abba_push_flag_paysize(ab=ab)))

        stats.update(self._compute_pure_acks_abba(ab=ab))

        stats.update(self._bidirectional_time_stats_to_unidirectional(
            suffix,
            self._compute_time_related_stats(direction_attribute_method(naming.TIMESTAMP))))

        return stats

    def _compute_stats(self) -> dict:
        stats = dict()
        stats.update(super()._compute_stats())

        stats.update(self._compute_unidirectional_stats(ab=True))
        stats.update(self._compute_unidirectional_stats(ab=False))

        return stats






