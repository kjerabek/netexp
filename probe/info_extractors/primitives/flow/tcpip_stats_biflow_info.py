from probe.info_extractors.primitives.flow.tcpip_base_extended_flow_info import TCPIPFlowBaseExtendedFlowInfo
from probe.info_extractors.primitives.packet.tcpip_packet_info import TCPIPPacketInfo
from probe.info_extractors.primitives.flow.tcpip_flow_info import TCPIPFlowInfo
from probe import constants

import numpy as np


class TCPIPStatsBiFlowInfo(TCPIPFlowBaseExtendedFlowInfo):
    which_packet = TCPIPPacketInfo

    def __init__(self, packet_info: TCPIPPacketInfo):
        super().__init__(packet_info)

    def _compute_all_stats(self, attribute_name: str, attributes: []) -> dict:
        stats = dict()

        attributes = np.array(attributes)
        stats['mean_' + attribute_name] = np.mean(attributes, axis=0)
        stats['std_' + attribute_name] = np.std(attributes, axis=0)
        stats['sum_' + attribute_name] = np.sum(attributes, axis=0)

        stats.update(self._compute_quartiles(attribute_name, attributes))

        return stats

    @staticmethod
    def _compute_no_payload(attributes: [], suffix: str = '') -> dict:
        stats = dict()
        stats['no_payload_num' + suffix] = attributes.count(0)

        return stats

    @staticmethod
    def _compute_quartiles(attribute_name: str, attributes: []) -> dict:
        stats = {}

        if len(attributes) == 0:
            attributes = [np.nan]

        minimum, quart1, median, quart3, maximum = np.nanpercentile(attributes, [0, 25, 50, 75, 100])
        stats['minimum_' + attribute_name] = minimum
        stats['quart1_' + attribute_name] = quart1
        stats['median_' + attribute_name] = median
        stats['quart3_' + attribute_name] = quart3
        stats['maximum_' + attribute_name] = maximum

        return stats

    @staticmethod
    def _compute_sums(attribute_name: str, attributes: []) -> dict:
        stats = dict()
        stats['sum_' + attribute_name] = sum(attributes)

        return stats

    @staticmethod
    def _timestamps_to_inter_arrival_times(timestamps: []) -> list:
        inter_arrivals = []

        if not len(timestamps):
            return inter_arrivals

        previous_timestamp = timestamps[0]

        for index in range(1, len(timestamps)):
            inter_arrivals.append(timestamps[index] - previous_timestamp)
            previous_timestamp = timestamps[index]

        return inter_arrivals

    @staticmethod
    def _compute_inter_arrival_times(timestamps: []) -> dict:
        stats = {}

        inter_arrivals = TCPIPStatsBiFlowInfo._timestamps_to_inter_arrival_times(timestamps)
        inter_arrivals = np.array(inter_arrivals)

        feature_name = 'inter_arrival_time'
        stats['mean_' + feature_name] = np.mean(inter_arrivals, axis=0)
        stats['std_' + feature_name] = np.std(inter_arrivals, axis=0)
        stats.update(TCPIPStatsBiFlowInfo._compute_quartiles(feature_name, inter_arrivals))

        return stats

    def _compute_time_related_stats(self, timestamps: []) -> dict:
        stats = dict()
        stats.update(self._compute_inter_arrival_times(timestamps))

        if len(timestamps):
            stats['duration'] = timestamps[-1] - timestamps[0]
            stats['start'] = timestamps[0]
        else:
            stats['duration'] = None
            stats['start'] = None

        return stats

    def _compute_idle(self, timestamps: []) -> dict:
        stats = dict()

        inter_arrival_times = self._timestamps_to_inter_arrival_times(timestamps)

        total_idle_time = 0
        total_time = 0
        for inter_arrival_time in inter_arrival_times:
            if inter_arrival_time > constants.IDLE_PERIOD:
                total_idle_time += inter_arrival_time

            total_time += inter_arrival_time

        stats['total_idle_time'] = total_idle_time

        if total_time:
            stats['percent_idle_time'] = 100 / total_time * total_idle_time
        else:
            stats['percent_idle_time'] = 0

        return stats

    def _compute_bulk(self, duration: int) -> dict:
        bulk_transaction_transitions_counter = 0
        tmp_bulk_packets_counter_a = 0
        tmp_bulk_packets_counter_b = 0
        src_ip = self.packets[0].src_ip
        total_bulk_time = 0
        first_bulk_packet_timestamp = 0
        last_bulk_packet_timestamp = 0

        for packet in self.packets_selection:
            if packet.src_ip == src_ip:
                if packet.paysize > 0:
                    if tmp_bulk_packets_counter_b > 3:
                        bulk_transaction_transitions_counter += 1
                        total_bulk_time = last_bulk_packet_timestamp - first_bulk_packet_timestamp

                    if tmp_bulk_packets_counter_a == 0:
                        first_bulk_packet_timestamp = packet.timestamp

                    last_bulk_packet_timestamp = packet.timestamp
                    tmp_bulk_packets_counter_a += 1
                    tmp_bulk_packets_counter_b = 0
            else:
                if packet.paysize > 0:
                    if tmp_bulk_packets_counter_a > 3:
                        bulk_transaction_transitions_counter += 1
                        total_bulk_time = last_bulk_packet_timestamp - first_bulk_packet_timestamp

                    if tmp_bulk_packets_counter_b == 0:
                        first_bulk_packet_timestamp = packet.timestamp

                    last_bulk_packet_timestamp = packet.timestamp
                    tmp_bulk_packets_counter_b += 1
                    tmp_bulk_packets_counter_a = 0

        if tmp_bulk_packets_counter_a > 3 or tmp_bulk_packets_counter_b > 3:
            bulk_transaction_transitions_counter += 1
            total_bulk_time = last_bulk_packet_timestamp - first_bulk_packet_timestamp

        stats = dict()
        stats['bulk_transaction_transitions'] = bulk_transaction_transitions_counter
        stats['total_bulk_time'] = total_bulk_time

        if duration:
            stats['percent_bulk_time'] = 100 / duration * total_bulk_time
        else:
            stats['percent_bulk_time'] = 0

        return stats

    def _get_packets_push_flag_paysize(self):
        attributes = []

        for packet in self.packets_selection:
            if packet.tcp_flag_psh:
                attributes.append(packet.paysize)

        return attributes

    def _compute_stats(self) -> dict:
        stats = dict()
        stats.update(TCPIPFlowInfo.to_dict(self))
        stats['num_packets'] = len(self.packets)

        for attribute_name in ['ip_header_len', 'trans_header_len', 'paysize']:
            stats.update(self._compute_all_stats(attribute_name, self._get_packets_attribute(attribute_name)))

        stats.update(self._compute_no_payload(self._get_packets_attribute('paysize')))

        for attribute_name in ['tcp_flag_psh', 'tcp_flag_urg', 'tcp_flag_rst', 'tcp_flag_ack',
                               'tcp_flag_fin', 'tcp_flag_syn']:
            stats.update(self._compute_sums(attribute_name, self._get_packets_attribute(attribute_name)))

        stats.update(self._compute_all_stats('psh_paysize', self._get_packets_push_flag_paysize()))

        timestamps = self._get_packets_attribute('timestamp')
        stats.update(self._compute_time_related_stats(timestamps))
        stats.update(self._compute_idle(timestamps))
        stats.update(self._compute_bulk(stats['duration']))

        return stats

    def to_dict(self) -> dict:
        return self._compute_stats()
