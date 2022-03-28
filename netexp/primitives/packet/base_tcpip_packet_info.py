from netexp.primitives.base_primitive import BasePrimitive

import dpkt
import socket
import json


class BaseTCPIPPacketInfo(BasePrimitive):
    flow_key = None
    timestamp = None

    # network layer
    src_ip = None
    dst_ip = None

    # transport layer
    sport = None
    dport = None
    proto = None

    tcp_ack = None
    tcp_seq = None
    tcp_flag_fin = None
    tcp_flag_syn = None
    tcp_flag_ack = None
    tcp_flag_rst = None

    def __init__(self, timestamp, packet):
        self.__extract_base_info(timestamp, packet)

    def __extract_base_info(self, timestamp, packet) -> None:
        self.timestamp = int(timestamp * 1000000)
        self.flow_timestamp_identifier = self.timestamp

        l3_layer = packet.data

        if not isinstance(l3_layer, dpkt.ip.IP) and not isinstance(l3_layer, dpkt.ip6.IP6):
            return

        self.__extract_ip_base_info(l3_layer)

        l4_layer = l3_layer.data

        if not isinstance(l4_layer, dpkt.tcp.TCP) and not isinstance(l4_layer, dpkt.udp.UDP):
            return

        self.__extract_transport_base_info(l4_layer)

        self.__set_flowkey(self.src_ip,
                           self.dst_ip,
                           self.sport,
                           self.dport,
                           self.proto)

    def __extract_ip_base_info(self, l3_layer) -> None:
        if isinstance(l3_layer, dpkt.ip.IP):
            self.src_ip = socket.inet_ntop(socket.AF_INET, l3_layer.src)
            self.dst_ip = socket.inet_ntop(socket.AF_INET, l3_layer.dst)
            return

        if isinstance(l3_layer, dpkt.ip6.IP6):
            self.src_ip = socket.inet_ntop(socket.AF_INET6, l3_layer.src)
            self.dst_ip = socket.inet_ntop(socket.AF_INET6, l3_layer.dst)
            return

    def __extract_transport_base_info(self, l4_layer) -> None:
        if isinstance(l4_layer, dpkt.tcp.TCP):
            self.proto = 'TCP'
            self.tcp_seq = l4_layer.seq
            self.tcp_ack = l4_layer.ack

            self.tcp_flag_fin = 1 if l4_layer.flags & dpkt.tcp.TH_FIN else 0
            self.tcp_flag_syn = 1 if l4_layer.flags & dpkt.tcp.TH_SYN else 0
            self.tcp_flag_ack = 1 if l4_layer.flags & dpkt.tcp.TH_ACK else 0
            self.tcp_flag_rst = 1 if l4_layer.flags & dpkt.tcp.TH_RST else 0

        if isinstance(l4_layer, dpkt.udp.UDP):
            self.proto = 'UDP'

        self.sport = l4_layer.sport
        self.dport = l4_layer.dport

    def __set_flowkey(self, src_ip: str, dst_ip: str,
                      sport: int, dport: int, proto: str) -> None:

        if src_ip == dst_ip:
            first_ip, second_ip = src_ip, dst_ip
            if sport < dport:
                first_port, second_port = sport, dport
            else:
                first_port, second_port = dport, sport
        elif src_ip < dst_ip:
            first_ip, second_ip = src_ip, dst_ip
            first_port, second_port = sport, dport
        else:
            first_ip, second_ip = dst_ip, src_ip
            first_port, second_port = dport, sport

        self.flow_key = f'{first_ip}-{second_ip}_{first_port}-{second_port}_{proto}'

    def to_dict(self) -> dict:
        packet_info_base = dict(
            flow_key=self.flow_key,
            time=self.timestamp,
            src_ip=self.src_ip,
            dst_ip=self.dst_ip,
            sport=self.sport,
            dport=self.dport,
            proto=self.proto,
        )

        return packet_info_base

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def __str__(self):
        return str(self.to_dict())
