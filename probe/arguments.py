from probe.info_extractors.primitives.flow import TCPIPChunkStatsBiFlowNoackInfo, AVAILABLE_FLOWS

import argparse


def get_flowformat_help(available_flow_formats):
    help_string = ''
    for index in range(0, len(available_flow_formats)):
        help_string += f'{index} - {available_flow_formats[index]["name"]}\n'
    return help_string


parser = argparse.ArgumentParser(description='NETEXP - Network exploration probe.',
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
                                  help=get_flowformat_help(AVAILABLE_FLOWS))
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

parsed_args = parser.parse_args()
