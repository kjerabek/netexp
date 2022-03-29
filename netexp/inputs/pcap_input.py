from netexp.inputs.base_input import BaseInput

import dpkt

class PcapInput(BaseInput):
    def __init__(self, file_path: str, filter: str = None):
        self.file_path = file_path
        self.filter = filter

        try:
            self._open_with_pcap()
        except:
            self._open_with_dpkt()
   
    def _open_with_pcap(self):
        import pcap

        self.pcap_reader = pcap.pcap(name=self.file_path, promisc=False, immediate=True)

        if self.filter:
            self.pcap_reader.setfilter(self.filter)

        self._set_l2_parser()

    def _open_with_dpkt(self):
        self.pcap_file = open(self.file_path, 'rb')

        try:
            self.pcap_reader = dpkt.pcapng.Reader(self.pcap_file)
        except:
            self.pcap_reader = dpkt.pcap.Reader(self.pcap_file)

        self._set_l2_parser()

    def _set_l2_parser(self):
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
