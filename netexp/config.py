from netexp.info_extractors import TcpIpFlowExtractor, PacketExtractor
from netexp.primitives.flow import AVAILABLE_FLOWS
from netexp.inputs import PcapInput, IfaceInput
from netexp.outputs import CsvOutput

import argparse
import warnings

warnings.filterwarnings('ignore')


class BaseConfig:
    flow_time_range = 1
    num_skipped_packets = 40
    num_packets_chunk = 40
    which_flow = None

    input = None
    extractor = None
    output = None


class Config(BaseConfig):

    def __init__(self):
        self.init()

    @staticmethod
    def get_flowformat_help(available_flow_formats):
        help_string = ''
        for index in range(0, len(available_flow_formats)):
            help_string += f'{index} - {available_flow_formats[index]["name"]}\n'
        return help_string

    def arguments_parse(self):
        parser = argparse.ArgumentParser(description='NETEXP - Network exploration netexp.',
                                         formatter_class=argparse.RawTextHelpFormatter)

        parser.add_argument('--net-filter',
                            type=str,
                            help='Network input packet filter in Berkley Packet Filter format.')
        parser.add_argument('--flow-termination-time',
                            type=int,
                            default=1,
                            help='Wait time before flow export after last received fin flagged packet.')
        parser.add_argument('--num-skipped-packets',
                            type=int,
                            default=40,
                            help='Number of skipped packets from beginning that are not included in stats computation'
                                 '(works only with combination of chunk flow formats).')
        parser.add_argument('--num-packets-chunk',
                            type=int,
                            default=40,
                            help='Number of packets in chunk that are included in stats computation'
                                 '(works only with combination of chunk flow formats).')

        input_group = parser.add_mutually_exclusive_group(required=True)
        input_group.add_argument('--in-file-name',
                                 type=str,
                                 help='Input file name (only .pcap and .pcapng files are supported).')
        input_group.add_argument('--interface-name',
                                 type=str,
                                 help='Input interface name.')

        flow_or_packet_group = parser.add_mutually_exclusive_group(required=True)
        flow_or_packet_group.add_argument('--flow-format',
                                          type=int,
                                          choices=range(0, len(AVAILABLE_FLOWS)),
                                          help=self.get_flowformat_help(AVAILABLE_FLOWS))
        flow_or_packet_group.add_argument('--packet-format',
                                          type=int,
                                          choices=[0],
                                          help='0 - Packet')

        output_group = parser.add_mutually_exclusive_group(required=True)
        output_group.add_argument('--csv-filename',
                                  type=str,
                                  help='Output CSV filename.')
        output_group.add_argument('--json-filename',
                                  type=str,
                                  help='Output JSON filename.')

        return parser.parse_args()

    @staticmethod
    def get_input(parsed_args):
        if parsed_args.in_file_name:
            input_obj = PcapInput(file_path=parsed_args.in_file_name, filter=parsed_args.net_filter)
        else:
            input_obj = IfaceInput(if_name=parsed_args.iface_name, filter=parsed_args.net_filter)

        return input_obj

    def get_extractor(self, parsed_args):
        if parsed_args.flow_format is not None:
            extractor_obj = TcpIpFlowExtractor(self)
        else:
            extractor_obj = PacketExtractor(self)

        return extractor_obj

    @staticmethod
    def get_output(parsed_args):
        output_obj = None

        if parsed_args.csv_filename:
            output_obj = CsvOutput(filename=parsed_args.csv_filename)

        return output_obj

    @staticmethod
    def get_flow_format(parsed_args):
        return AVAILABLE_FLOWS[parsed_args.flow_format]['class']

    def init(self):
        parsed_args = self.arguments_parse()
        self.flow_time_range = parsed_args.flow_termination_time  # in seconds
        self.num_skipped_packets = parsed_args.num_skipped_packets
        self.num_packets_chunk = parsed_args.num_packets_chunk
        self.which_flow = self.get_flow_format(parsed_args)

        self.input = self.get_input(parsed_args)
        self.extractor = self.get_extractor(parsed_args)
        self.output = self.get_output(parsed_args)
