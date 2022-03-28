from tests.primitives.flow.probe_tcpip_flow_base import ProbeTCPIPFlowBase

from netexp.primitives.flow import TCPIPChunkStatsBiFlowNoackInfo
from netexp.common import naming


class TestTCPIPChunkStatsBiFlowNoack(ProbeTCPIPFlowBase):

    flow_class = TCPIPChunkStatsBiFlowNoackInfo

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

        assert 84.57 < stats[naming.MEAN_L4_PAYSIZE] < 84.58
        assert 77.16 < stats[naming.STD_L4_PAYSIZE] < 77.161
        assert 5953.74 < stats[naming.VAR_L4_PAYSIZE] < 5953.75
        assert stats[naming.SUM_L4_PAYSIZE] == 3383
        assert stats[naming.MIN_L4_PAYSIZE] == 31
        assert stats[naming.QUARTILE1_L4_PAYSIZE] == 39
        assert stats[naming.MED_L4_PAYSIZE] == 56
        assert stats[naming.QUARTILE3_L4_PAYSIZE] == 85
        assert stats[naming.MAX_L4_PAYSIZE] == 372

        assert stats[naming.NO_PAYLOAD_PACKETS] == 0
        assert stats[naming.SUM_TCP_FLAG_PSH] == 40
        assert stats[naming.SUM_TCP_FLAG_URG] == 0
        assert stats[naming.SUM_TCP_FLAG_RST] == 0
        assert stats[naming.SUM_TCP_FLAG_ACK] == 40
        assert stats[naming.SUM_TCP_FLAG_FIN] == 0
        assert stats[naming.SUM_TCP_FLAG_SYN] == 0
        assert stats[naming.PURE_ACKS_SENT] == 0

        assert 84.57 < stats[naming.MEAN_PSH_PACKETS_L4_PAYSIZE] < 84.58
        assert 77.16 < stats[naming.STD_PSH_PACKETS_L4_PAYSIZE] < 77.161
        assert 5953.74 < stats[naming.VAR_PSH_PACKETS_L4_PAYSIZE] < 5953.75
        assert stats[naming.SUM_PSH_PACKETS_L4_PAYSIZE] == 3383
        assert stats[naming.MIN_PSH_PACKETS_L4_PAYSIZE] == 31
        assert stats[naming.QUARTILE1_PSH_PACKETS_L4_PAYSIZE] == 39
        assert stats[naming.MED_PSH_PACKETS_L4_PAYSIZE] == 56
        assert stats[naming.QUARTILE3_PSH_PACKETS_L4_PAYSIZE] == 85
        assert stats[naming.MAX_PSH_PACKETS_L4_PAYSIZE] == 372

        assert 2444.2 < stats[naming.MEAN_INTER_ARRIVAL_TIME] < 2444.21
        assert 10286.91 < stats[naming.STD_INTER_ARRIVAL_TIME] < 10286.92
        assert 105820620.419 < stats[naming.VAR_INTER_ARRIVAL_TIME] < 105820620.42
        assert stats[naming.MIN_INTER_ARRIVAL_TIME] == 6
        assert stats[naming.QUARTILE1_INTER_ARRIVAL_TIME] == 13
        assert stats[naming.MED_INTER_ARRIVAL_TIME] == 71
        assert stats[naming.QUARTILE3_INTER_ARRIVAL_TIME] == 328
        assert stats[naming.MAX_INTER_ARRIVAL_TIME] == 64268

        assert stats[naming.DURATION] == 95324
        assert stats[naming.FIRST_TIMESTAMP] == 1590076145600006
        assert stats[naming.TIME_SPENT_IDLE] == 0
        assert stats[naming.PERCENT_IDLE_TIME] == 0.0

        assert stats[naming.BULK_TRANSACTION_TRANSITIONS] == 3
        assert stats[naming.TIME_SPENT_IN_BULK] == 85144
        assert 89.32 < stats[naming.PERCENT_BULK_TIME] < 89.33
