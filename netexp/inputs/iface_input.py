from netexp.inputs.base_input import BaseInput

import dpkt

class IfaceInput(BaseInput):
    def __init__(self, if_name: str = None, filter: str = None):
        self.if_name = if_name
        self.filter = filter

    def _setup_sniffer(self):
        import pcap

        self.pcap_reader = pcap.pcap(name=self.if_name, promisc=True, immediate=True)

        if self.filter:
            self.pcap_reader.setfilter(self.filter)

        self._set_l2_parser()

    def _set_l2_parser(self):
        if self.pcap_reader.datalink() == dpkt.pcap.DLT_LINUX_SLL:
            self.l2_parser = dpkt.sll.SLL
        else:
            self.l2_parser = dpkt.ethernet.Ethernet

    def __iter__(self):
        for timestamp, buffer in self.reader:
            pkt = self.l2_parser(buffer)

            yield timestamp, pkt

    def __next__(self):
        return next(iter(self))
