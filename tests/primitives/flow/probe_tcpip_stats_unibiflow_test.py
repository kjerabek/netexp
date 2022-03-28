from tests.primitives.flow import probe_tcpip_stats_biflow_test

from netexp.primitives.flow import TCPIPStatsUniBiFlowInfo
from netexp.common import naming


class TestTCPIPStatsUniBiFlow(probe_tcpip_stats_biflow_test.TestTCPIPStatsBiFlow):

    flow_class = TCPIPStatsUniBiFlowInfo

    def test_short_flow_ab_ba_stats(self, probe_short_flow):
        probe_short_flow.run()
        processed_flow = self.output.send.call_args.args[0]
        stats = processed_flow.to_dict()

        assert stats[naming.TOTAL_PACKETS_AB] == 7

        assert stats[naming.MEAN_L3_HEADER_LENGTH_AB] == 20.0
        assert stats[naming.STD_L3_HEADER_LENGTH_AB] == 0.0
        assert stats[naming.VAR_L3_HEADER_LENGTH_AB] == 0
        assert stats[naming.SUM_L3_HEADER_LENGTH_AB] == 140
        assert stats[naming.MIN_L3_HEADER_LENGTH_AB] == 20
        assert stats[naming.QUARTILE1_L3_HEADER_LENGTH_AB] == 20
        assert stats[naming.MED_L3_HEADER_LENGTH_AB] == 20
        assert stats[naming.QUARTILE3_L3_HEADER_LENGTH_AB] == 20
        assert stats[naming.MAX_L3_HEADER_LENGTH_AB] == 20

        assert 33.14 < stats[naming.MEAN_L4_HEADER_LENGTH_AB] < 33.15
        assert 2.79 < stats[naming.STD_L4_HEADER_LENGTH_AB] < 2.8
        assert 7.83 < stats[naming.VAR_L4_HEADER_LENGTH_AB] < 7.84
        assert stats[naming.SUM_L4_HEADER_LENGTH_AB] == 232
        assert stats[naming.MIN_L4_HEADER_LENGTH_AB] == 32
        assert stats[naming.QUARTILE1_L4_HEADER_LENGTH_AB] == 32
        assert stats[naming.MED_L4_HEADER_LENGTH_AB] == 32
        assert stats[naming.QUARTILE3_L4_HEADER_LENGTH_AB] == 32
        assert stats[naming.MAX_L4_HEADER_LENGTH_AB] == 40

        assert 73.8 < stats[naming.MEAN_L4_PAYSIZE_AB] < 73.9
        assert 180.91 < stats[naming.STD_L4_PAYSIZE_AB] < 180.92
        assert 32729.26 < stats[naming.VAR_L4_PAYSIZE_AB] < 32729.27
        assert stats[naming.SUM_L4_PAYSIZE_AB] == 517
        assert stats[naming.MIN_L4_PAYSIZE_AB] == 0
        assert stats[naming.QUARTILE1_L4_PAYSIZE_AB] == 0
        assert stats[naming.MED_L4_PAYSIZE_AB] == 0
        assert stats[naming.QUARTILE3_L4_PAYSIZE_AB] == 0
        assert stats[naming.MAX_L4_PAYSIZE_AB] == 517

        assert stats[naming.NO_PAYLOAD_PACKETS_AB] == 6
        assert stats[naming.SUM_TCP_FLAG_PSH_AB] == 1
        assert stats[naming.SUM_TCP_FLAG_RST_AB] == 0
        assert stats[naming.SUM_TCP_FLAG_ACK_AB] == 6
        assert stats[naming.SUM_TCP_FLAG_FIN_AB] == 1
        assert stats[naming.SUM_TCP_FLAG_SYN_AB] == 1

        assert stats[naming.MEAN_PSH_PACKETS_L4_PAYSIZE_AB] == 517.0
        assert stats[naming.STD_PSH_PACKETS_L4_PAYSIZE_AB] == 0.0
        assert stats[naming.VAR_PSH_PACKETS_L4_PAYSIZE_AB] == 0
        assert stats[naming.SUM_PSH_PACKETS_L4_PAYSIZE_AB] == 517
        assert stats[naming.MIN_PSH_PACKETS_L4_PAYSIZE_AB] == 517
        assert stats[naming.QUARTILE1_PSH_PACKETS_L4_PAYSIZE_AB] == 517
        assert stats[naming.MED_PSH_PACKETS_L4_PAYSIZE_AB] == 517
        assert stats[naming.QUARTILE3_PSH_PACKETS_L4_PAYSIZE_AB] == 517
        assert stats[naming.MAX_PSH_PACKETS_L4_PAYSIZE_AB] == 517

        assert stats[naming.PURE_ACKS_SENT_AB] == 4

        assert stats[naming.MEAN_INTER_ARRIVAL_TIME_AB] == 238039.0
        assert 519144.81 < stats[naming.STD_INTER_ARRIVAL_TIME_AB] < 519144.82
        assert 269511337554.32 < stats[naming.VAR_INTER_ARRIVAL_TIME_AB] < 269511337554.34
        assert stats[naming.MIN_INTER_ARRIVAL_TIME_AB] == 60
        assert stats[naming.QUARTILE1_INTER_ARRIVAL_TIME_AB] == 2459
        assert stats[naming.MED_INTER_ARRIVAL_TIME_AB] == 3475
        assert stats[naming.QUARTILE3_INTER_ARRIVAL_TIME_AB] == 19913
        assert stats[naming.MAX_INTER_ARRIVAL_TIME_AB] == 1398791

        assert stats[naming.TOTAL_PACKETS_BA] == 5

        assert stats[naming.MEAN_L3_HEADER_LENGTH_BA] == 20.0
        assert stats[naming.STD_L3_HEADER_LENGTH_BA] == 0.0
        assert stats[naming.VAR_L3_HEADER_LENGTH_BA] == 0
        assert stats[naming.SUM_L3_HEADER_LENGTH_BA] == 100
        assert stats[naming.MIN_L3_HEADER_LENGTH_BA] == 20
        assert stats[naming.QUARTILE1_L3_HEADER_LENGTH_BA] == 20
        assert stats[naming.MED_L3_HEADER_LENGTH_BA] == 20
        assert stats[naming.QUARTILE3_L3_HEADER_LENGTH_BA] == 20
        assert stats[naming.MAX_L3_HEADER_LENGTH_BA] == 20

        assert stats[naming.MEAN_L4_HEADER_LENGTH_BA] == 33.6
        assert 3.19 < stats[naming.STD_L4_HEADER_LENGTH_BA] < 3.21
        assert 10.238 < stats[naming.VAR_L4_HEADER_LENGTH_BA] < 10.24
        assert stats[naming.SUM_L4_HEADER_LENGTH_BA] == 168
        assert stats[naming.MIN_L4_HEADER_LENGTH_BA] == 32
        assert stats[naming.QUARTILE1_L4_HEADER_LENGTH_BA] == 32
        assert stats[naming.MED_L4_HEADER_LENGTH_BA] == 32
        assert stats[naming.QUARTILE3_L4_HEADER_LENGTH_BA] == 32
        assert stats[naming.MAX_L4_HEADER_LENGTH_BA] == 40

        assert 631.5 < stats[naming.MEAN_L4_PAYSIZE_BA] < 631.7
        assert 780.22 < stats[naming.STD_L4_PAYSIZE_BA] < 780.23
        assert 608746.23 < stats[naming.VAR_L4_PAYSIZE_BA] < 608746.25
        assert stats[naming.SUM_L4_PAYSIZE_BA] == 3158
        assert stats[naming.MIN_L4_PAYSIZE_BA] == 0
        assert stats[naming.QUARTILE1_L4_PAYSIZE_BA] == 0
        assert stats[naming.MED_L4_PAYSIZE_BA] == 0
        assert stats[naming.QUARTILE3_L4_PAYSIZE_BA] == 1418
        assert stats[naming.MAX_L4_PAYSIZE_BA] == 1740

        assert stats[naming.NO_PAYLOAD_PACKETS_BA] == 3
        assert stats[naming.SUM_TCP_FLAG_PSH_BA] == 1
        assert stats[naming.SUM_TCP_FLAG_RST_BA] == 0
        assert stats[naming.SUM_TCP_FLAG_ACK_BA] == 5
        assert stats[naming.SUM_TCP_FLAG_FIN_BA] == 1
        assert stats[naming.SUM_TCP_FLAG_SYN_BA] == 1

        assert stats[naming.MEAN_PSH_PACKETS_L4_PAYSIZE_BA] == 1740.0
        assert stats[naming.STD_PSH_PACKETS_L4_PAYSIZE_BA] == 0.0
        assert stats[naming.VAR_PSH_PACKETS_L4_PAYSIZE_BA] == 0
        assert stats[naming.SUM_PSH_PACKETS_L4_PAYSIZE_BA] == 1740
        assert stats[naming.MIN_PSH_PACKETS_L4_PAYSIZE_BA] == 1740
        assert stats[naming.QUARTILE1_PSH_PACKETS_L4_PAYSIZE_BA] == 1740
        assert stats[naming.MED_PSH_PACKETS_L4_PAYSIZE_BA] == 1740
        assert stats[naming.QUARTILE3_PSH_PACKETS_L4_PAYSIZE_BA] == 1740
        assert stats[naming.MAX_PSH_PACKETS_L4_PAYSIZE_BA] == 1740

        assert stats[naming.PURE_ACKS_SENT_BA] == 1

        assert stats[naming.MEAN_INTER_ARRIVAL_TIME_BA] == 356195.0
        assert 604004.63 < stats[naming.STD_INTER_ARRIVAL_TIME_BA] < 604004.64
        assert 364821595492.4 < stats[naming.VAR_INTER_ARRIVAL_TIME_BA] < 364821595492.6
        assert stats[naming.MIN_INTER_ARRIVAL_TIME_BA] == 58
        assert stats[naming.QUARTILE1_INTER_ARRIVAL_TIME_BA] == 5921
        assert stats[naming.MED_INTER_ARRIVAL_TIME_BA] == 16489
        assert stats[naming.QUARTILE3_INTER_ARRIVAL_TIME_BA] == 16489
        assert stats[naming.MAX_INTER_ARRIVAL_TIME_BA] == 1402312

