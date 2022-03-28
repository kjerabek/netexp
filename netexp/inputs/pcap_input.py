from netexp.inputs.base_input import BaseInput

import dpkt

# todo
class PcapInput(BaseInput):
    def __init__(self, file_path: str, filter: str = ""):
        self.file_path = file_path
        self.filter = filter
        self.pcap_file = open(file_path, 'rb')

        try:
            self.pcap_reader = dpkt.pcapng.Reader(self.pcap_file)
        except:
            self.pcap_reader = dpkt.pcap.Reader(self.pcap_file)

        if self.pcap_reader.datalink() == dpkt.pcap.DLT_LINUX_SLL:
            self.l2_parser = dpkt.sll.SLL
        else:
            self.l2_parser = dpkt.ethernet.Ethernet

    def __iter__(self):
        for timestamp, buffer in self.pcap_reader:
            pkt = self.l2_parser(buffer)

            yield timestamp, pkt

    def __next__(self):
        return next(iter(self))
