from tests.common.constants import PATH_PCAP_SHORT_PROPER, PATH_PCAP_IDLE_BULK, PATH_PCAP_LONG_DOH

import pytest


class ProbeTCPIPFlowBase:

    flow_class = None
    argparse = None
    extractor_process_packet_method = None
    output = None

    def init_probe(self, mocker, pcap_file_name):
        self.argparse = mocker.Mock()
        mocker.patch('argparse.ArgumentParser', self.argparse)
        from netexp.config import BaseConfig
        mocker.patch('netexp.config.Config', BaseConfig)

        from netexp.probe import Probe
        from netexp.inputs.pcap_input import PcapInput
        from netexp.info_extractors.tcpip_flow_extractor import TcpIpFlowExtractor

        self.extractor_process_packet_method = mocker.Mock()
        self.output = mocker.Mock()
        probe = Probe()
        probe.config.input = PcapInput(file_path=pcap_file_name)
        probe.config.which_flow = self.flow_class
        probe.config.extractor = TcpIpFlowExtractor(probe.config)
        probe.config.output = self.output
        probe.init_components()

        return probe

    @pytest.fixture()
    def probe_short_flow(self, mocker):
        probe = self.init_probe(mocker, PATH_PCAP_SHORT_PROPER)

        yield probe

    @pytest.fixture()
    def probe_long_doh_flow(self, mocker):
        probe = self.init_probe(mocker, PATH_PCAP_LONG_DOH)

        yield probe

    @pytest.fixture()
    def probe_idle_bulk_flow(self, mocker):
        probe = self.init_probe(mocker, PATH_PCAP_IDLE_BULK)

        yield probe
