from tests.primitives.flow.probe_tcpip_flow_base import ProbeTCPIPFlowBase

from netexp.primitives.flow import TCPIPStatsBiFlowInfo
from netexp.common import naming


class TestTCPIPStatsBiFlow(ProbeTCPIPFlowBase):

    flow_class = TCPIPStatsBiFlowInfo

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

        assert stats[naming.MEAN_L3_HEADER_LENGTH] == 20.0
        assert stats[naming.STD_L3_HEADER_LENGTH] == 0.0
        assert stats[naming.VAR_L3_HEADER_LENGTH] == 0
        assert stats[naming.SUM_L3_HEADER_LENGTH] == 240
        assert stats[naming.MIN_L3_HEADER_LENGTH] == 20.0
        assert stats[naming.QUARTILE1_L3_HEADER_LENGTH] == 20.0
        assert stats[naming.MED_L3_HEADER_LENGTH] == 20.0
        assert stats[naming.QUARTILE3_L3_HEADER_LENGTH] == 20.0
        assert stats[naming.MAX_L3_HEADER_LENGTH] == 20.0

        assert 33.3 < stats[naming.MEAN_L4_HEADER_LENGTH] < 33.4
        assert 2.9 < stats[naming.STD_L4_HEADER_LENGTH] < 3.0
        assert 8.88 < stats[naming.VAR_L4_HEADER_LENGTH] < 8.89
        assert stats[naming.SUM_L4_HEADER_LENGTH] == 400
        assert stats[naming.MIN_L4_HEADER_LENGTH] == 32.0
        assert stats[naming.QUARTILE1_L4_HEADER_LENGTH] == 32.0
        assert stats[naming.MED_L4_HEADER_LENGTH] == 32.0
        assert stats[naming.QUARTILE3_L4_HEADER_LENGTH] == 32.0
        assert stats[naming.MAX_L4_HEADER_LENGTH] == 40.0

        assert 306.2 < stats[naming.MEAN_L4_PAYSIZE] < 306.3
        assert 590.2 < stats[naming.STD_L4_PAYSIZE] < 590.22
        assert 348345.35 < stats[naming.VAR_L4_PAYSIZE] < 348345.36
        assert stats[naming.SUM_L4_PAYSIZE] == 3675
        assert stats[naming.MIN_L4_PAYSIZE] == 0.0
        assert stats[naming.QUARTILE1_L4_PAYSIZE] == 0.0
        assert stats[naming.MED_L4_PAYSIZE] == 0.0
        assert stats[naming.QUARTILE3_L4_PAYSIZE] == 0.0
        assert stats[naming.MAX_L4_PAYSIZE] == 1740

        assert stats[naming.NO_PAYLOAD_PACKETS] == 9
        assert stats[naming.SUM_TCP_FLAG_PSH] == 2
        assert stats[naming.SUM_TCP_FLAG_URG] == 0
        assert stats[naming.SUM_TCP_FLAG_RST] == 0
        assert stats[naming.SUM_TCP_FLAG_ACK] == 11
        assert stats[naming.SUM_TCP_FLAG_FIN] == 2
        assert stats[naming.SUM_TCP_FLAG_SYN] == 2

        assert stats[naming.MEAN_PSH_PACKETS_L4_PAYSIZE] == 1128.5
        assert stats[naming.STD_PSH_PACKETS_L4_PAYSIZE] == 611.5
        assert 373932.24 < stats[naming.VAR_PSH_PACKETS_L4_PAYSIZE] < 373932.26
        assert stats[naming.SUM_PSH_PACKETS_L4_PAYSIZE] == 2257
        assert stats[naming.MIN_PSH_PACKETS_L4_PAYSIZE] == 517
        assert stats[naming.QUARTILE1_PSH_PACKETS_L4_PAYSIZE] == 517
        assert stats[naming.MED_PSH_PACKETS_L4_PAYSIZE] == 517
        assert stats[naming.QUARTILE3_PSH_PACKETS_L4_PAYSIZE] == 1740
        assert stats[naming.MAX_PSH_PACKETS_L4_PAYSIZE] == 1740

        assert 129839.45 < stats[naming.MEAN_INTER_ARRIVAL_TIME] < 129839.46
        assert 401303.39 < stats[naming.STD_INTER_ARRIVAL_TIME] < 401303.4
        assert 161044418688.79 < stats[naming.VAR_INTER_ARRIVAL_TIME] < 161044418688.8
        assert stats[naming.MIN_INTER_ARRIVAL_TIME] == 19
        assert stats[naming.QUARTILE1_INTER_ARRIVAL_TIME] == 36
        assert stats[naming.MED_INTER_ARRIVAL_TIME] == 2459
        assert stats[naming.QUARTILE3_INTER_ARRIVAL_TIME] == 3500
        assert stats[naming.MAX_INTER_ARRIVAL_TIME] == 1398791

        assert stats[naming.DURATION] == 1428234
        assert stats[naming.FIRST_TIMESTAMP] == 1590076139670363
        assert stats[naming.TIME_SPENT_IDLE] == 0
        assert stats[naming.PERCENT_IDLE_TIME] == 0
        assert stats[naming.BULK_TRANSACTION_TRANSITIONS] == 0
        assert stats[naming.TIME_SPENT_IN_BULK] == 0
        assert stats[naming.PERCENT_BULK_TIME] == 0
        assert stats[naming.PURE_ACKS_SENT] == 5

    def test_bulk_idle_single_flow_stats(self, probe_idle_bulk_flow):
        probe_idle_bulk_flow.run()
        processed_flow = self.output.send.call_args.args[0]
        stats = processed_flow.to_dict()

        assert stats[naming.DURATION] == 4461220
        assert stats[naming.TIME_SPENT_IDLE] == 3651981
        assert 81.85 < stats[naming.PERCENT_IDLE_TIME] < 81.87
        assert stats[naming.BULK_TRANSACTION_TRANSITIONS] == 6
        assert stats[naming.TIME_SPENT_IN_BULK] == 12279
        assert 0.274 < stats[naming.PERCENT_BULK_TIME] < 0.276
