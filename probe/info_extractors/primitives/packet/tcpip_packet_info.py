from probe.info_extractors.primitives.packet.base_tcpip_packet_info import BaseTCPIPPacketInfo

import dpkt
import json


class TCPIPPacketInfo(BaseTCPIPPacketInfo):
    # network layer
    ttl = None  # or ipv6 hop limit
    tos = None  # or ipv6 traffic class
    ip_header_len = None
    ip_paysize = None

    # TODO add options for tcp/udp/ip

    # transport layer
    tcp_window = None
    tcp_flag_psh = None
    tcp_flag_urg = None
    tcp_flag_ece = None
    tcp_flag_crw = None

    trans_header_len = None
    paysize = None

    def __init__(self, timestamp, packet):
        super().__init__(timestamp, packet)
        self.__extract_info(packet)

    def __extract_info(self, packet) -> None:

        l4_layer = packet.data

        if not self.src_ip:
            return

        self.__extract_ip_info(l4_layer)

        l3_layer = l4_layer.data

        if not self.sport:
            return

        self.__extract_transport_info(l3_layer)

    def __extract_transport_info(self, l4_layer) -> None:
        if isinstance(l4_layer, dpkt.tcp.TCP):
            self.__extract_tcp_info(l4_layer)

        self.paysize = len(l4_layer.data)
        self.trans_header_len = self.ip_paysize - self.paysize

    def __extract_tcp_info(self, l4_layer) -> None:
        self.tcp_window = l4_layer.win
        self.tcp_flag_psh = 1 if l4_layer.flags & dpkt.tcp.TH_PUSH else 0
        self.tcp_flag_urg = 1 if l4_layer.flags & dpkt.tcp.TH_URG else 0
        self.tcp_flag_ece = 1 if l4_layer.flags & dpkt.tcp.TH_ECE else 0
        self.tcp_flag_crw = 1 if l4_layer.flags & dpkt.tcp.TH_CWR else 0

    def __extract_ip_info(self, l3_layer) -> None:
        if isinstance(l3_layer, dpkt.ip6.IP6):
            self.__extract_ipv6_info(l3_layer)

        if isinstance(l3_layer, dpkt.ip.IP):
            self.__extract_ipv4_info(l3_layer)

        self.ip_paysize = len(l3_layer.data)
        self.ip_header_len = len(l3_layer) - self.ip_paysize

    def __extract_ipv4_info(self, l3_layer) -> None:
        self.tos = l3_layer.tos
        self.ttl = l3_layer.ttl

    def __extract_ipv6_info(self, l3_layer) -> None:
        #self.tos = ip_layer.tc
        self.ttl = l3_layer.hlim
        self.ip_paysize = l3_layer.plen

    def to_dict(self):
        base_packet_info = super().to_dict()
        packet_info = dict(
            ttl=self.ttl,
            tos=self.tos,
            ip_header_len=self.ip_header_len,
            paysize=self.paysize,
            tcp_window=self.tcp_window,
            tcp_ack=self.tcp_ack,
            tcp_seq=self.tcp_seq,
            tcp_flag_fin=self.tcp_flag_fin,
            tcp_flag_syn=self.tcp_flag_syn,
            tcp_flag_rst=self.tcp_flag_rst,
            tcp_flag_psh=self.tcp_flag_psh,
            tcp_flag_ack=self.tcp_flag_ack,
            tcp_flag_urg=self.tcp_flag_urg,
            tcp_flag_ece=self.tcp_flag_ece,
            tcp_flag_crw=self.tcp_flag_crw,
            trans_header_len=self.trans_header_len,
        )

        base_packet_info.update(packet_info)

        return packet_info

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return str(self.to_dict())
