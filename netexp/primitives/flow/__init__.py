from netexp.primitives.flow.tcpip_flow_info import TCPIPFlowInfo
from netexp.primitives.flow.tcpip_extended_biflow_info import TCPIPFlowExtendedBiFlowInfo
from netexp.primitives.flow.tcpip_extended_unibiflow_info import TCPIPFlowExtendedUniBiFlowInfo
from netexp.primitives.flow.tcpip_stats_biflow_info import TCPIPStatsBiFlowInfo
from netexp.primitives.flow.tcpip_stats_unibiflow_info import TCPIPStatsUniBiFlowInfo
from netexp.primitives.flow.tcpip_stats_biflow_noack_info import TCPIPStatsBiFlowNoackInfo

from netexp.primitives.flow.tcpip_chunk_biflow_info import \
    TCPIPChunkBiFlowInfo
from netexp.primitives.flow.tcpip_chunk_biflow_noack_info import \
    TCPIPChunkBiFlowNoackInfo
from netexp.primitives.flow.tcpip_chunk_stats_biflow_info import \
    TCPIPChunkStatsBiFlowInfo
from netexp.primitives.flow.tcpip_chunk_stats_biflow_noack_info import \
    TCPIPChunkStatsBiFlowNoackInfo


import sys
import inspect


def get_available_classes():
    available_classes = []

    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            available_classes.append({'name': obj.__name__, 'class': obj})

    return available_classes


AVAILABLE_FLOWS = get_available_classes()
