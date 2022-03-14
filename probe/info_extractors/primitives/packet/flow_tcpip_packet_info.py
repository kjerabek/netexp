from probe.info_extractors.primitives.packet.tcpip_packet_info import TCPIPPacketInfo

import json


class FlowTCPIPPacketInfo(TCPIPPacketInfo):
    flow_identifier = None
    flow_timestamp_identifier = None

    def __init__(self, timestamp, packet):
        super().__init__(timestamp, packet)
        self.flow_timestamp_identifier = self.timestamp

        if not self.has_transport_layer():
            return

        self.update_identifier()

    def has_transport_layer(self) -> bool:
        if self.sport is not None:
            return True

        return False

    def update_identifier(self) -> None:
        self.flow_identifier = f'{self.flow_timestamp_identifier}_{self.flow_key}'

    def to_dict(self):
        flow_packet_info = dict(
            flow_identifier=self.flow_identifier,
            flow_timestamp_identifier=self.flow_timestamp_identifier,
        )
        flow_packet_info.update(super().to_dict())

        return flow_packet_info

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return str(self.to_dict())
