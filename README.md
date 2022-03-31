# NetExP
Network Exploration Probe - Simple network exploration probe written in Python. The probe process network traffic, work directly with packets or group packets to flows and extract and export statistical or other features.

The probe architecture provides easy way to extend functionality mainly in form of primitives (packets, flows). It provides playground for easy alternative feature exploration.

Some of the currently supported extracted features from flows can be found in [[1]](#1).

## Installation

At first, clone the repository.

Then install requirements.

```
$ pip install -r requirements.txt
```

Project utilizes `dpkt` and `pcap-ct` python libraries. Unfortunately `pcap-ct` library is not compatible with MacOS, hence the functionality is limited on MacOS, but the pcap files can be processed.


## Usage

The tool provides command line interface with followin options.

```
usage: netexp-cli [-h] [--net-filter NET_FILTER] [--flow-termination-time FLOW_TERMINATION_TIME] [--num-skipped-packets NUM_SKIPPED_PACKETS]
                  [--num-packets-chunk NUM_PACKETS_CHUNK] (--in-file-name IN_FILE_NAME | --interface-name INTERFACE_NAME)
                  (--flow-format {0,1,2,3,4,5,6,7,8,9} | --packet-format {0}) (--csv-filename CSV_FILENAME | --json-filename JSON_FILENAME)

NETEXP - Network exploration netexp.

optional arguments:
  -h, --help            show this help message and exit
  --net-filter NET_FILTER
                        Network input packet filter in Berkley Packet Filter format.
  --flow-termination-time FLOW_TERMINATION_TIME
                        Wait time before flow export after last received fin flagged packet.
  --num-skipped-packets NUM_SKIPPED_PACKETS
                        Number of skipped packets from beginning that are not included in stats computation(works only with combination of chunk flow formats).
  --num-packets-chunk NUM_PACKETS_CHUNK
                        Number of packets in chunk that are included in stats computation(works only with combination of chunk flow formats).
  --in-file-name IN_FILE_NAME
                        Input file name (only .pcap and .pcapng files are supported).
  --interface-name INTERFACE_NAME
                        Input interface name.
  --flow-format {0,1,2,3,4,5,6,7,8,9}
                        0 - TCPIPChunkBiFlowInfo
                        1 - TCPIPChunkBiFlowNoackInfo
                        2 - TCPIPChunkStatsBiFlowInfo
                        3 - TCPIPChunkStatsBiFlowNoackInfo
                        4 - TCPIPFlowExtendedBiFlowInfo
                        5 - TCPIPFlowExtendedUniBiFlowInfo
                        6 - TCPIPFlowInfo
                        7 - TCPIPStatsBiFlowInfo
                        8 - TCPIPStatsBiFlowNoackInfo
                        9 - TCPIPStatsUniBiFlowInfo
  --packet-format {0}   0 - Packet
  --csv-filename CSV_FILENAME
                        Output CSV filename.
  --json-filename JSON_FILENAME
                        Output JSON filename.
```


## References

<a id="1">[1]</a> 
MOORE, Andrew; ZUEV, Denis; CROGAN, Michael. Discriminators for use in flow-based classification. 2013.
