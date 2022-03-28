from tests.primitives.flow.probe_tcpip_flow_base import ProbeTCPIPFlowBase

from netexp.primitives.flow import TCPIPFlowInfo
from netexp.common import naming

import json


class TestTCPIPFlowInfo(ProbeTCPIPFlowBase):

    flow_class = TCPIPFlowInfo

    def test_short_proper_pcap_single_flow_internals(self, probe_short_flow):
        probe_short_flow.run()
        processed_flow = self.output.send.call_args.args[0]

        assert processed_flow.num_fin_flags == 2
        assert processed_flow.num_rst_flags == 0
        assert processed_flow.num_packets_from_first_rst == 0
        assert processed_flow.last_fin_seq == 791347748
        assert processed_flow.last_packet_timestamp == 1590076141098597
        assert len(processed_flow.packets) == 12

    def test_short_proper_pcap_single_flow_to_dict(self, probe_short_flow):
        probe_short_flow.run()
        processed_flow = self.output.send.call_args.args[0]
        processed_flow_dict = processed_flow.to_dict()

        assert isinstance(processed_flow_dict, dict)
        assert len(processed_flow_dict.keys()) == 6
        assert processed_flow_dict[naming.FLOW_KEY] == '172.17.0.2-8.8.4.4_59088-443_TCP'
        assert processed_flow_dict[naming.SRC_IP] == '172.17.0.2'
        assert processed_flow_dict[naming.DST_IP] == '8.8.4.4'
        assert processed_flow_dict[naming.SPORT] == 59088
        assert processed_flow_dict[naming.DPORT] == 443
        assert processed_flow_dict[naming.PROTO] == 'TCP'

    def test_short_proper_pcap_single_flow_json(self, probe_short_flow):
        probe_short_flow.run()
        processed_flow = self.output.send.call_args.args[0]
        processed_flow_dict = json.loads(processed_flow.to_json())

        assert isinstance(processed_flow_dict, dict)
        assert len(processed_flow_dict.keys()) == 6
        assert processed_flow_dict[naming.FLOW_KEY] == '172.17.0.2-8.8.4.4_59088-443_TCP'
        assert processed_flow_dict[naming.SRC_IP] == '172.17.0.2'
        assert processed_flow_dict[naming.DST_IP] == '8.8.4.4'
        assert processed_flow_dict[naming.SPORT] == 59088
        assert processed_flow_dict[naming.DPORT] == 443
        assert processed_flow_dict[naming.PROTO] == 'TCP'

    def test_long_doh_pcap_single_flow_internals(self, probe_long_doh_flow):
        probe_long_doh_flow.run()
        processed_flow = self.output.send.call_args.args[0]

        assert processed_flow.num_fin_flags == 2
        assert processed_flow.num_rst_flags == 0
        assert processed_flow.num_packets_from_first_rst == 0
        assert processed_flow.last_fin_seq == 2101150149
        assert processed_flow.last_packet_timestamp == 1590076155429694
        assert len(processed_flow.packets) == 1614

    def test_long_doh_pcap_single_flow_to_dict(self, probe_long_doh_flow):
        probe_long_doh_flow.run()
        processed_flow = self.output.send.call_args.args[0]
        processed_flow_dict = processed_flow.to_dict()

        assert isinstance(processed_flow_dict, dict)
        assert len(processed_flow_dict.keys()) == 6
        assert processed_flow_dict[naming.FLOW_KEY] == '172.17.0.2-8.8.8.8_33010-443_TCP'
        assert processed_flow_dict[naming.SRC_IP] == '172.17.0.2'
        assert processed_flow_dict[naming.DST_IP] == '8.8.8.8'
        assert processed_flow_dict[naming.SPORT] == 33010
        assert processed_flow_dict[naming.DPORT] == 443
        assert processed_flow_dict[naming.PROTO] == 'TCP'

