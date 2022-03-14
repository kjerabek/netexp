from probe.info_extractors.base_extractor import BaseExtractor
from probe.info_extractors.primitives.packet.base_tcpip_packet_info import BaseTCPIPPacketInfo

from probe import config


class TcpIpFlowExtractor(BaseExtractor):
    def __init__(self):
        self.flows = {}
        self.unfinished_flows = []
        self.finished_flows = []
        self.last_timestamp = 0
        self.time_range_unfinished = config.flow_time_range * 1000000
        self.Flow = config.which_flow

    def process_packet(self, timestamp, packet):
        packet_info = self.Flow.which_packet(timestamp, packet)
        self.last_timestamp = packet_info.timestamp

        if packet_info.proto == 'TCP':
            self.__add_packet(packet_info)

    def __add_packet(self, packet_info: BaseTCPIPPacketInfo):
        if self.__is_new_flow_start(packet_info):
            self.__finish_flow_if_already_exists(packet_info)
            self.__add_new_flow(packet_info)
        else:
            self.__add_packet_to_existing_flow(packet_info)
            self.__finish_unfinished_flows()

    @staticmethod
    def __is_new_flow_start(packet_info: BaseTCPIPPacketInfo) -> bool:
        return packet_info.tcp_flag_syn == 1 and packet_info.tcp_flag_ack == 0

    def __finish_flow_if_already_exists(self, packet_info: BaseTCPIPPacketInfo):
        if packet_info.flow_key in self.flows.keys():
            finished_flow = self.flows.pop(packet_info.flow_key)

            self.finished_flows.append(finished_flow)

    def __add_new_flow(self, packet_info: BaseTCPIPPacketInfo):
        flow = self.Flow(packet_info)
        self.flows[packet_info.flow_key] = flow

    def __add_packet_to_existing_flow(self, packet_info: BaseTCPIPPacketInfo):
        if packet_info.flow_key in self.flows.keys():
            self.__add_packet_to_flows(packet_info)
        else:
            self.__add_packet_to_unfinished_flows(packet_info)

    def __finish_unfinished_flows(self):
        if len(self.unfinished_flows) == 0:
            return

        index = 0

        while index < len(self.unfinished_flows):
            if (self.last_timestamp - self.unfinished_flows[index].last_packet_timestamp) > self.time_range_unfinished:
                finished_flow = self.unfinished_flows.pop(index)
                self.finished_flows.append(finished_flow)
                index -= 1
            else:
                break

            index += 1

    def __add_packet_to_flows(self, packet_info: BaseTCPIPPacketInfo):
        flow = self.flows[packet_info.flow_key]
        flow.add_packet(packet_info)

        if flow.complete:
            unfinished_flow = self.flows.pop(packet_info.flow_key)
            self.unfinished_flows.append(unfinished_flow)

    def __add_packet_to_unfinished_flows(self, packet_info: BaseTCPIPPacketInfo):
        for index in range(0, len(self.unfinished_flows), -1):
            if self.unfinished_flows[index].flow_key == packet_info.flow_key:
                unfinished_flow = self.unfinished_flows.pop(index)
                unfinished_flow.add_packet(packet_info)
                self.unfinished_flows.append(unfinished_flow)
                break

    def pop_processed(self):
        finished_flows = [flow for flow in self.finished_flows]
        self.finished_flows.clear()
        return finished_flows

    def pop_rest(self):
        rest = [self.flows[key] for key in self.flows.keys()]
        rest.extend(self.unfinished_flows)
        rest.extend(self.finished_flows)

        self.flows.clear()
        self.unfinished_flows.clear()
        self.finished_flows.clear()

        return rest
