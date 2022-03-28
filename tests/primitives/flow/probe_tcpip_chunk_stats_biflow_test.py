from tests.primitives.flow.probe_tcpip_flow_base import ProbeTCPIPFlowBase

from netexp.primitives.flow import TCPIPChunkStatsBiFlowInfo
from netexp.common import naming


class TestTCPIPChunkStatsBiFlow(ProbeTCPIPFlowBase):

    flow_class = TCPIPChunkStatsBiFlowInfo

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

    def test_long_doh_flow_stats(self, probe_long_doh_flow):
        probe_long_doh_flow.run()
        processed_flow = self.output.send.call_args.args[0]
        stats = processed_flow.to_dict()

        assert isinstance(stats, dict)
        assert stats[naming.CHUNK_TOTAL_PACKETS] == 40
        assert stats[naming.PROCESSED_PACKETS_IN_CHUNK] == 40
        assert stats[naming.TOTAL_PACKETS] == 1614
        assert stats[naming.MEAN_L3_HEADER_LENGTH] == 20.0
        assert stats[naming.STD_L3_HEADER_LENGTH] == 0.0
        assert stats[naming.VAR_L3_HEADER_LENGTH] == 0
        assert stats[naming.SUM_L3_HEADER_LENGTH] == 800
        assert stats[naming.MIN_L3_HEADER_LENGTH] == 20
        assert stats[naming.QUARTILE1_L3_HEADER_LENGTH] == 20
        assert stats[naming.MED_L3_HEADER_LENGTH] == 20
        assert stats[naming.QUARTILE3_L3_HEADER_LENGTH] == 20
        assert stats[naming.MAX_L3_HEADER_LENGTH] == 20
        assert stats[naming.MEAN_L4_HEADER_LENGTH] == 32.0
        assert stats[naming.STD_L4_HEADER_LENGTH] == 0.0
        assert stats[naming.VAR_L4_HEADER_LENGTH] == 0
        assert stats[naming.SUM_L4_HEADER_LENGTH] == 1280
        assert stats[naming.MIN_L4_HEADER_LENGTH] == 32
        assert stats[naming.QUARTILE1_L4_HEADER_LENGTH] == 32
        assert stats[naming.MED_L4_HEADER_LENGTH] == 32
        assert stats[naming.QUARTILE3_L4_HEADER_LENGTH] == 32
        assert stats[naming.MAX_L4_HEADER_LENGTH] == 32

        assert stats[naming.MEAN_L4_PAYSIZE] == 65.175
        assert stats[naming.STD_L4_PAYSIZE] == 85.3190739225409
        assert 7279.34 < stats[naming.VAR_L4_PAYSIZE] < 7279.35
        assert stats[naming.SUM_L4_PAYSIZE] == 2607
        assert stats[naming.MIN_L4_PAYSIZE] == 0
        assert stats[naming.QUARTILE1_L4_PAYSIZE] == 0
        assert stats[naming.MED_L4_PAYSIZE] == 39
        assert stats[naming.QUARTILE3_L4_PAYSIZE] == 78
        assert stats[naming.MAX_L4_PAYSIZE] == 372

        assert stats[naming.NO_PAYLOAD_PACKETS] == 11
        assert stats[naming.SUM_TCP_FLAG_PSH] == 29
        assert stats[naming.SUM_TCP_FLAG_URG] == 0
        assert stats[naming.SUM_TCP_FLAG_RST] == 0
        assert stats[naming.SUM_TCP_FLAG_ACK] == 40
        assert stats[naming.SUM_TCP_FLAG_FIN] == 0
        assert stats[naming.SUM_TCP_FLAG_SYN] == 0

        assert 89.89 < stats[naming.MEAN_PSH_PACKETS_L4_PAYSIZE] < 89.9
        assert 88.419 < stats[naming.STD_PSH_PACKETS_L4_PAYSIZE] < 88.42
        assert 7818.08 < stats[naming.VAR_PSH_PACKETS_L4_PAYSIZE] < 7818.1
        assert stats[naming.SUM_PSH_PACKETS_L4_PAYSIZE] == 2607
        assert stats[naming.MIN_PSH_PACKETS_L4_PAYSIZE] == 31
        assert stats[naming.QUARTILE1_PSH_PACKETS_L4_PAYSIZE] == 39
        assert stats[naming.MED_PSH_PACKETS_L4_PAYSIZE] == 56
        assert stats[naming.QUARTILE3_PSH_PACKETS_L4_PAYSIZE] == 85
        assert stats[naming.MAX_PSH_PACKETS_L4_PAYSIZE] == 372

        assert 2270.79 < stats[naming.MEAN_INTER_ARRIVAL_TIME] < 2270.8
        assert 8848.29 < stats[naming.STD_INTER_ARRIVAL_TIME] < 8848.3
        assert 78292332.57 < stats[naming.VAR_INTER_ARRIVAL_TIME] < 78292332.58
        assert stats[naming.MIN_INTER_ARRIVAL_TIME] == 6
        assert stats[naming.QUARTILE1_INTER_ARRIVAL_TIME] == 13
        assert stats[naming.MED_INTER_ARRIVAL_TIME] == 95
        assert stats[naming.QUARTILE3_INTER_ARRIVAL_TIME] == 376
        assert stats[naming.MAX_INTER_ARRIVAL_TIME] == 55313
        assert stats[naming.DURATION] == 88561
        assert stats[naming.FIRST_TIMESTAMP] == 1590076145600006
        assert stats[naming.TIME_SPENT_IDLE] == 0
        assert stats[naming.PERCENT_IDLE_TIME] == 0.0

        assert stats[naming.BULK_TRANSACTION_TRANSITIONS] == 3
        assert stats[naming.TIME_SPENT_IN_BULK] == 78709
        assert 88.87 < stats[naming.PERCENT_BULK_TIME] < 88.88
