from abc import ABC, abstractmethod


class BaseExtractor(ABC):
    @abstractmethod
    def process_packet(self, timestamp, packet):
        pass

    @abstractmethod
    def pop_processed(self):
        pass

    @abstractmethod
    def pop_rest(self):
        pass
