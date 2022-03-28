from netexp.primitives.packet.base_tcpip_packet_info import BaseTCPIPPacketInfo
from netexp.primitives.base_primitive import BasePrimitive

from netexp.common import naming

import json


class WrongPacketPassed(Exception):
    pass


class NotFirstFlowPacket(Exception):
    pass


class TCPIPFlowInfo(BasePrimitive):
    which_packet = BaseTCPIPPacketInfo

    packets = None
    complete = False
    started = False
    flow_key = None

    num_fin_flags = 0
    num_rst_flags = 0
    num_packets_from_first_rst = 0
    last_fin_seq = 0

    last_packet_timestamp = 0

    def __init__(self, packet_info: BaseTCPIPPacketInfo, config):
        self.config = config
        if not isinstance(packet_info, self.which_packet):
            raise WrongPacketPassed

        if packet_info.tcp_flag_syn != 1 or packet_info.tcp_flag_ack != 0:
            raise NotFirstFlowPacket

        self.packets = []
        self.packets.append(packet_info)
        self.last_packet_timestamp = packet_info.timestamp
        self.flow_key = packet_info.flow_key
        self.complete = False

    def add_packet(self, packet_info: BaseTCPIPPacketInfo) -> None:
        if not isinstance(packet_info, self.which_packet):
            raise WrongPacketPassed

        self.__check_finished(packet_info)

        self.packets.append(packet_info)
        self.last_packet_timestamp = packet_info.timestamp

    def __check_finished(self, packet_info: BaseTCPIPPacketInfo) -> None:
        if packet_info.tcp_flag_rst:
            self.num_rst_flags += 1
            self.complete = True
            return

        # normally finished including retransmission
        if self.num_fin_flags >= 2:
            if packet_info.tcp_flag_fin == 0 and packet_info.tcp_flag_ack == 1:
                if packet_info.tcp_seq == self.packets[-1].tcp_ack:
                    self.complete = True

        if packet_info.tcp_flag_fin:
            if self.last_fin_seq != packet_info.tcp_seq:
                self.num_fin_flags += 1
                self.last_fin_seq = packet_info.tcp_seq

    def to_dict(self) -> dict:
        stats = dict()

        stats[naming.FLOW_KEY] = self.packets[0].flow_key
        stats[naming.SRC_IP] = self.packets[0].src_ip
        stats[naming.DST_IP] = self.packets[0].dst_ip
        stats[naming.SPORT] = self.packets[0].sport
        stats[naming.DPORT] = self.packets[0].dport
        stats[naming.PROTO] = self.packets[0].proto

        return stats

    def to_json(self):
        return json.dumps(self.to_dict())
