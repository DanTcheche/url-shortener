from abc import ABC, abstractmethod


class EncodeStrategy(ABC):

    @abstractmethod
    def encode(self, text):
        pass
