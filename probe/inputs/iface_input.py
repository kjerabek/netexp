from probe.inputs.base_input import BaseInput

import dpkt
import pcap

# todo
class IfaceInput(BaseInput):
    def __init__(self, if_name: str = None, filter: str = None):
        self.reader = pcap.pcap()
        self.filter = filter

        if filter:
            self.reader.setfilter(filter)

        if if_name:
            self.l2_parser = dpkt.ethernet.Ethernet
        else:
            self.l2_parser = dpkt.sll.SLL

    def __iter__(self):
        for timestamp, buffer in self.reader:
            pkt = self.l2_parser(buffer)

            yield timestamp, pkt

    def __next__(self):
        return next(iter(self))
