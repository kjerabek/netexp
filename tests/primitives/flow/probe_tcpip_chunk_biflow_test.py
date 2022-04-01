from tests.primitives.flow.probe_tcpip_flow_base import ProbeTCPIPFlowBase

from netexp.primitives.flow import TCPIPChunkBiFlowInfo
from netexp.common import naming


class TestTCPIPChunkBiFlow(ProbeTCPIPFlowBase):

    flow_class = TCPIPChunkBiFlowInfo

    def test_long_doh_flow_stats(self, probe_long_doh_flow):
        probe_long_doh_flow.run()
        processed_flow = self.output.send.call_args.args[0]
        stats = processed_flow.to_dict()

        assert isinstance(stats, dict)
        assert stats[naming.PROTO] == 'TCP'
        assert stats[f'0_{naming.ATTRIBUTE}'] == -367000
        assert stats[f'1_{naming.ATTRIBUTE}'] == -31000
        assert stats[f'35_{naming.ATTRIBUTE}'] == 0
        assert stats[f'38_{naming.ATTRIBUTE}'] == -31000
        assert stats[f'39_{naming.ATTRIBUTE}'] == -39000
