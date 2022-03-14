from abc import ABC, abstractmethod


class BaseOutput(ABC):

    @abstractmethod
    def send(self, packet_info: any):
        pass

    @abstractmethod
    def write_record(self, packet_info: any):
        pass
