from tests.primitives.flow.probe_tcpip_flow_base import ProbeTCPIPFlowBase

from netexp.primitives.flow import TCPIPFlowExtendedBiFlowInfo
from netexp.common import naming


class TestTCPIPExtendedBiFlow(ProbeTCPIPFlowBase):

    flow_class = TCPIPFlowExtendedBiFlowInfo

    def test_short_single_flow_internals(self, probe_short_flow):
        probe_short_flow.run()
        processed_flow = self.output.send.call_args.args[0]

        assert processed_flow.num_fin_flags == 2
        assert processed_flow.num_rst_flags == 0
        assert processed_flow.num_packets_from_first_rst == 0
        assert processed_flow.last_fin_seq == 791347748
        assert processed_flow.last_packet_timestamp == 1590076141098597
        assert len(processed_flow.packets) == 12

    def test_short_single_flow_stats(self, probe_short_flow):
        probe_short_flow.run()
        processed_flow = self.output.send.call_args.args[0]
        stats = processed_flow.to_dict()

        assert isinstance(stats, dict)
        assert stats[naming.TOTAL_PACKETS] == 12
        assert len(stats[naming.TIMESTAMP]) == 12
        assert stats[naming.TIMESTAMP][0] == 1590076139670363
        assert stats[naming.TIMESTAMP][-1] == 1590076141098597
        assert stats[naming.TCP_FLAG_PSH] == [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]
        assert stats[naming.TCP_FLAG_SYN] == [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert stats[naming.TCP_FLAG_FIN] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0]
        assert stats[naming.TCP_FLAG_ACK] == [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        assert stats[naming.L4_PAYSIZE] == [0, 0, 0, 517, 0, 1418, 0, 1740, 0, 0, 0, 0]
        assert stats[naming.PACKET_DIRECTIONS] == [1, -1, 1, 1, -1, -1, 1, -1, 1, 1, -1, 1]
        assert stats[naming.L3_HEADER_LENGTH] == [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20]
        assert stats[naming.L4_HEADER_LENGTH] == [40, 40, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32]
