from abc import ABC, abstractmethod


class BasePrimitive(ABC):

    @abstractmethod
    def to_dict(self):
        pass

    @abstractmethod
    def to_json(self):
        pass
