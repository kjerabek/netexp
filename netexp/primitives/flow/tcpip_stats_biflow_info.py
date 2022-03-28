from netexp.primitives.flow.tcpip_base_extended_flow_info import TCPIPFlowBaseExtendedFlowInfo
from netexp.primitives.packet.tcpip_packet_info import TCPIPPacketInfo
from netexp.primitives.flow.tcpip_flow_info import TCPIPFlowInfo
from netexp.common import constants
from netexp.common import naming

import numpy as np


class TCPIPStatsBiFlowInfo(TCPIPFlowBaseExtendedFlowInfo):
    which_packet = TCPIPPacketInfo

    def __init__(self, packet_info: TCPIPPacketInfo, config):
        super().__init__(packet_info, config)

    def _compute_all_stats(self, attribute_name: str, attributes: []) -> dict:
        stats = dict()

        attributes = np.array(attributes)
        stats[naming.VAR_PREFIX + attribute_name] = np.var(attributes, axis=0)
        stats[naming.MEAN_PREFIX + attribute_name] = np.mean(attributes, axis=0)
        stats[naming.STD_PREFIX + attribute_name] = np.std(attributes, axis=0)
        stats[naming.SUM_PREFIX + attribute_name] = np.sum(attributes, axis=0)

        stats.update(self._compute_quartiles(attribute_name, attributes))

        return stats

    @staticmethod
    def _compute_no_payload(attributes: [], suffix: str = '') -> dict:
        stats = dict()
        stats[naming.NO_PAYLOAD_PACKETS + suffix] = attributes.count(0)

        return stats

    @staticmethod
    def _compute_quartiles(attribute_name: str, attributes: []) -> dict:
        stats = {}

        if len(attributes) == 0:
            attributes = [np.nan]

        minimum, q1, median, q3, maximum = np.nanpercentile(attributes,
                                                            [constants.MIN_PERCENTILE,
                                                             constants.QUARTILE1_PERCENTILE,
                                                             constants.MED_PERCENTILE,
                                                             constants.QUARTILE3_PERCENTILE,
                                                             constants.MAX_PERCENTILE],
                                                            method='nearest')
        stats[naming.MIN_PREFIX + attribute_name] = minimum
        stats[naming.QUARTILE1_PREFIX + attribute_name] = q1
        stats[naming.MED_PREFIX + attribute_name] = median
        stats[naming.QUARTILE3_PREFIX + attribute_name] = q3
        stats[naming.MAX_PREFIX + attribute_name] = maximum

        return stats

    @staticmethod
    def _compute_sums(attribute_name: str, attributes: []) -> dict:
        stats = dict()
        stats[naming.SUM_PREFIX + attribute_name] = sum(attributes)

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

        feature_name = naming.INTER_ARRIVAL_TIME
        stats[naming.MEAN_PREFIX + feature_name] = np.mean(inter_arrivals, axis=0)
        stats[naming.STD_PREFIX + feature_name] = np.std(inter_arrivals, axis=0)
        stats[naming.VAR_PREFIX + feature_name] = np.var(inter_arrivals, axis=0)
        stats.update(TCPIPStatsBiFlowInfo._compute_quartiles(feature_name, inter_arrivals))

        return stats

    def _compute_time_related_stats(self, timestamps: []) -> dict:
        stats = dict()
        stats.update(self._compute_inter_arrival_times(timestamps))

        if len(timestamps):
            stats[naming.DURATION] = timestamps[-1] - timestamps[0]
            stats[naming.FIRST_TIMESTAMP] = timestamps[0]
        else:
            stats[naming.DURATION] = None
            stats[naming.FIRST_TIMESTAMP] = None

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

        stats[naming.TIME_SPENT_IDLE] = total_idle_time

        if total_time:
            stats[naming.PERCENT_IDLE_TIME] = 100 / total_time * total_idle_time
        else:
            stats[naming.PERCENT_IDLE_TIME] = 0

        return stats

    @staticmethod
    def __count_transaction_bulk_transitions(bulktrans_transitions: [], all_trans_counter: int) -> int:
        bulk_transaction_transitions_counter = 0

        for index in range(0, len(bulktrans_transitions)):
            if bulktrans_transitions[index] == 0:
                continue
            if index == 0:
                if bulktrans_transitions[index] != 0:
                    bulk_transaction_transitions_counter += 1
            else:
                if (bulktrans_transitions[index] - bulktrans_transitions[index-1]) != 1:
                    bulk_transaction_transitions_counter += 2

        if bulktrans_transitions:
            if bulktrans_transitions[-1] != all_trans_counter:
                bulk_transaction_transitions_counter += 1

        return bulk_transaction_transitions_counter

    def _compute_bulk(self, duration: int) -> dict:
        bulk_transaction_transitions = []
        tmp_bulk_packets_counter_a = 0
        tmp_bulk_packets_counter_b = 0
        src_ip = self.packets[0].src_ip
        total_bulk_time = 0
        first_bulk_packet_timestamp = 0
        last_bulk_packet_timestamp = 0
        all_trans_counter = -1

        for packet in self.packets_selection:
            if packet.src_ip == src_ip:
                if packet.paysize > 0:
                    if tmp_bulk_packets_counter_b > 3:
                        bulk_transaction_transitions.append(all_trans_counter)
                        total_bulk_time += last_bulk_packet_timestamp - first_bulk_packet_timestamp

                    if tmp_bulk_packets_counter_a == 0:
                        all_trans_counter += 1
                        first_bulk_packet_timestamp = packet.timestamp

                    last_bulk_packet_timestamp = packet.timestamp
                    tmp_bulk_packets_counter_a += 1
                    tmp_bulk_packets_counter_b = 0
            else:
                if packet.paysize > 0:
                    if tmp_bulk_packets_counter_a > 3:
                        bulk_transaction_transitions.append(all_trans_counter)
                        total_bulk_time += last_bulk_packet_timestamp - first_bulk_packet_timestamp

                    if tmp_bulk_packets_counter_b == 0:
                        all_trans_counter += 1
                        first_bulk_packet_timestamp = packet.timestamp

                    last_bulk_packet_timestamp = packet.timestamp
                    tmp_bulk_packets_counter_a = 0
                    tmp_bulk_packets_counter_b += 1

        if tmp_bulk_packets_counter_a > 3 or tmp_bulk_packets_counter_b > 3:
            bulk_transaction_transitions.append(all_trans_counter)
            total_bulk_time += last_bulk_packet_timestamp - first_bulk_packet_timestamp

        bulk_transaction_transitions_counter = self.__count_transaction_bulk_transitions(bulk_transaction_transitions,
                                                                                         all_trans_counter)

        stats = dict()
        stats[naming.BULK_TRANSACTION_TRANSITIONS] = bulk_transaction_transitions_counter
        stats[naming.TIME_SPENT_IN_BULK] = total_bulk_time

        if duration:
            stats[naming.PERCENT_BULK_TIME] = 100 / duration * total_bulk_time
        else:
            stats[naming.PERCENT_BULK_TIME] = 0

        return stats

    def _get_packets_push_flag_paysize(self) -> list:
        attributes = []

        for packet in self.packets_selection:
            if packet.tcp_flag_psh:
                attributes.append(packet.paysize)

        return attributes

    def _compute_pure_acks(self) -> dict:
        stats = dict()
        ack_counter = 0

        for packet in self.packets_selection:
            if packet.tcp_flag_ack and packet.paysize == 0 and not packet.tcp_flag_fin and \
                    not packet.tcp_flag_rst and not packet.tcp_flag_syn:
                ack_counter += 1

        stats[naming.PURE_ACKS_SENT] = ack_counter

        return stats

    def _compute_stats(self) -> dict:
        stats = dict()
        stats.update(TCPIPFlowInfo.to_dict(self))
        stats[naming.TOTAL_PACKETS] = len(self.packets)

        for attribute_name in [naming.L3_HEADER_LENGTH, naming.L4_HEADER_LENGTH, naming.L4_PAYSIZE]:
            stats.update(self._compute_all_stats(attribute_name, self._get_packets_attribute(attribute_name)))

        stats.update(self._compute_no_payload(self._get_packets_attribute(naming.L4_PAYSIZE)))

        for attribute_name in [naming.TCP_FLAG_PSH, naming.TCP_FLAG_URG, naming.TCP_FLAG_RST,
                               naming.TCP_FLAG_ACK, naming.TCP_FLAG_FIN, naming.TCP_FLAG_SYN]:
            stats.update(self._compute_sums(attribute_name, self._get_packets_attribute(attribute_name)))

        stats.update(self._compute_pure_acks())
        stats.update(self._compute_all_stats(naming.PSH_PACKETS_L4_PAYSIZE, self._get_packets_push_flag_paysize()))

        timestamps = self._get_packets_attribute(naming.TIMESTAMP)
        stats.update(self._compute_time_related_stats(timestamps))
        stats.update(self._compute_idle(timestamps))
        stats.update(self._compute_bulk(stats[naming.DURATION]))

        return stats

    def to_dict(self) -> dict:
        return self._compute_stats()
