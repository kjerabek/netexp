from probe.info_extractors.primitives.flow import AVAILABLE_FLOWS
from probe.inputs import PcapInput#, IfaceInput
from probe.info_extractors import TcpIpFlowExtractor, PacketExtractor
from probe.outputs import CsvOutput
from probe.arguments import parsed_args

import warnings

warnings.filterwarnings('ignore')


def get_input(parsed_args):
    input_obj = None

    if parsed_args.in_file_name:
        input_obj = PcapInput(file_path=parsed_args.in_file_name, filter=parsed_args.net_filter)
    #else:
    #    input_obj = IfaceInput(if_name=parsed_args.iface_name, filter=parsed_args.net_filter)

    return input_obj


def get_extractor(parsed_args):
    if parsed_args.flow_format:
        extractor_obj = TcpIpFlowExtractor()
    else:
        extractor_obj = PacketExtractor()

    return extractor_obj


def get_output(parsed_args):
    output_obj = None

    if parsed_args.csv_filename:
        output_obj = CsvOutput(filename=parsed_args.csv_filename)

    return output_obj


flow_time_range = parsed_args.flow_termination_time  # in seconds
num_skipped_packets = parsed_args.num_skipped_packets
num_packets_chunk = parsed_args.num_packets_chunk
which_flow = AVAILABLE_FLOWS[parsed_args.flow_format]['class']

input = get_input(parsed_args)
extractor = get_extractor(parsed_args)
output = get_output(parsed_args)
