from probe.info_extractors.primitives.flow.tcpip_extended_biflow_info import TCPIPFlowExtendedBiFlowInfo
from probe.info_extractors.primitives.packet.tcpip_packet_info import TCPIPPacketInfo


class TCPIPFlowExtendedUniBiFlowInfo(TCPIPFlowExtendedBiFlowInfo):
    which_packet = TCPIPPacketInfo

    def __init__(self, packet_info: TCPIPPacketInfo):
        super().__init__(packet_info)

    def _extract_stats(self) -> dict:
        stats = dict()
        stats.update(TCPIPFlowExtendedBiFlowInfo.to_dict(self))

        attributes = ['timestamp', 'ip_header_len', 'trans_header_len',
                      'paysize', 'tcp_flag_psh', 'tcp_flag_rst', 'tcp_flag_ack',
                      'tcp_flag_fin', 'tcp_flag_syn']

        for attribute_name in attributes:
            stats[attribute_name + '_ab'] = self._get_ab_attributes(attribute_name)

        for attribute_name in attributes:
            stats[attribute_name + '_ba'] = self._get_ba_attributes(attribute_name)

        return stats

    def to_dict(self) -> dict:
        return self._extract_stats()
