from probe.info_extractors.primitives.flow.tcpip_stats_biflow_info import TCPIPStatsBiFlowInfo
from probe.info_extractors.primitives.packet.tcpip_packet_info import TCPIPPacketInfo


class TCPIPStatsUniBiFlowInfo(TCPIPStatsBiFlowInfo):
    which_packet = TCPIPPacketInfo

    def __init__(self, packet_info: TCPIPPacketInfo):
        super().__init__(packet_info)

    def _get_ab_push_flag_paysize(self):
        attributes = []
        src_ip = self.packets[0].src_ip

        for packet in self.packets:
            if packet.src_ip == src_ip and packet.tcp_flag_psh:
                attributes.append(packet.paysize)

        return attributes

    def _get_ba_push_flag_paysize(self):
        attributes = []
        src_ip = self.packets[0].src_ip

        for packet in self.packets:
            if packet.src_ip != src_ip and packet.tcp_flag_psh:
                attributes.append(packet.paysize)

        return attributes

    def _compute_stats(self) -> dict:
        stats = dict()
        stats.update(super()._compute_stats())
        stats['num_packets_ab'] = len(self._get_ab_attributes('paysize'))
        stats['num_packets_ba'] = len(self._get_ba_attributes('paysize'))

        # ab

        for attribute_name in ['ip_header_len', 'trans_header_len', 'paysize']:
            stats.update(self._compute_all_stats(attribute_name + '_ab',
                                                 self._get_ab_attributes(attribute_name)))

        stats.update(self._compute_no_payload(self._get_ab_attributes('paysize'), suffix='_ab'))

        for attribute_name in ['tcp_flag_psh', 'tcp_flag_rst', 'tcp_flag_ack', 'tcp_flag_fin', 'tcp_flag_syn']:
            stats.update(self._compute_sums(attribute_name + '_ab',
                                            self._get_ab_attributes(attribute_name)))

        stats.update(self._compute_all_stats('psh_paysize_ab', self._get_ab_push_flag_paysize()))

        # ba

        for attribute_name in ['ip_header_len', 'trans_header_len', 'paysize']:
            stats.update(self._compute_all_stats(attribute_name + '_ba',
                                                 self._get_ba_attributes(attribute_name)))

        stats.update(self._compute_no_payload(self._get_ba_attributes('paysize'), suffix='_ba'))

        for attribute_name in ['tcp_flag_psh', 'tcp_flag_rst', 'tcp_flag_ack', 'tcp_flag_fin', 'tcp_flag_syn']:
            stats.update(self._compute_sums(attribute_name + '_ba',
                                            self._get_ba_attributes(attribute_name)))

        stats.update(self._compute_all_stats('psh_paysize_ba', self._get_ba_push_flag_paysize()))
        return stats






