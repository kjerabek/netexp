from netexp.primitives.flow.tcpip_extended_biflow_info import TCPIPFlowExtendedBiFlowInfo
from netexp.primitives.packet.tcpip_packet_info import TCPIPPacketInfo

from netexp.common import naming


class TCPIPFlowExtendedUniBiFlowInfo(TCPIPFlowExtendedBiFlowInfo):
    which_packet = TCPIPPacketInfo

    def __init__(self, packet_info: TCPIPPacketInfo, config):
        super().__init__(packet_info, config)

    def _extract_stats(self) -> dict:
        stats = dict()
        stats.update(TCPIPFlowExtendedBiFlowInfo.to_dict(self))

        attributes = [naming.TIMESTAMP, naming.L3_HEADER_LENGTH, naming.L4_HEADER_LENGTH,
                      naming.L4_PAYSIZE, naming.TCP_FLAG_PSH, naming.TCP_FLAG_RST,
                      naming.TCP_FLAG_ACK, naming.TCP_FLAG_FIN, naming.TCP_FLAG_SYN]

        for attribute_name in attributes:
            stats[attribute_name + naming.SUFFIX_AB] = self._get_ab_attributes(attribute_name)

        for attribute_name in attributes:
            stats[attribute_name + naming.SUFFIX_BA] = self._get_ba_attributes(attribute_name)

        return stats

    def to_dict(self) -> dict:
        return self._extract_stats()
