from tests.primitives.flow import probe_tcpip_extended_biflow_test

from netexp.primitives.flow import TCPIPFlowExtendedUniBiFlowInfo
from netexp.common import naming


class TestTCPIPExtendedUniBiFlow(probe_tcpip_extended_biflow_test.TestTCPIPExtendedBiFlow):

    flow_class = TCPIPFlowExtendedUniBiFlowInfo

    def test_short_single_uni_flow_stats(self, probe_short_flow):
        probe_short_flow.run()
        processed_flow = self.output.send.call_args.args[0]
        stats = processed_flow.to_dict()

        assert stats[naming.TIMESTAMP_AB] == [1590076139670363, 1590076139673838, 1590076139676297, 1590076139696210,
                                              1590076139696270, 1590076141095061, 1590076141098597]
        assert stats[naming.L3_HEADER_LENGTH_AB] == [20, 20, 20, 20, 20, 20, 20]
        assert stats[naming.L4_HEADER_LENGTH_AB] == [40, 32, 32, 32, 32, 32, 32]
        assert stats[naming.L4_PAYSIZE_AB] == [0, 0, 517, 0, 0, 0, 0]
        assert stats[naming.TCP_FLAG_PSH_AB] == [0, 0, 1, 0, 0, 0, 0]
        assert stats[naming.TCP_FLAG_RST_AB] == [0, 0, 0, 0, 0, 0, 0]
        assert stats[naming.TCP_FLAG_ACK_AB] == [0, 1, 1, 1, 1, 1, 1]
        assert stats[naming.TCP_FLAG_FIN_AB] == [0, 0, 0, 0, 0, 1, 0]
        assert stats[naming.TCP_FLAG_SYN_AB] == [1, 0, 0, 0, 0, 0, 0]
        assert stats[naming.TIMESTAMP_BA] == [1590076139673781, 1590076139679702, 1590076139696191, 1590076139696249,
                                              1590076141098561]
        assert stats[naming.L3_HEADER_LENGTH_BA] == [20, 20, 20, 20, 20]
        assert stats[naming.L4_HEADER_LENGTH_BA] == [40, 32, 32, 32, 32]
        assert stats[naming.L4_PAYSIZE_BA] == [0, 0, 1418, 1740, 0]
        assert stats[naming.TCP_FLAG_PSH_BA] == [0, 0, 0, 1, 0]
        assert stats[naming.TCP_FLAG_RST_BA] == [0, 0, 0, 0, 0]
        assert stats[naming.TCP_FLAG_ACK_BA] == [1, 1, 1, 1, 1]
        assert stats[naming.TCP_FLAG_FIN_BA] == [0, 0, 0, 0, 1]
        assert stats[naming.TCP_FLAG_SYN_BA] == [1, 0, 0, 0, 0]
