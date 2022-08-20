from abc import ABC, abstractmethod


class Storage(ABC):
    @property
    @abstractmethod
    def get_last_id(self):
        raise NotImplementedError

    @abstractmethod
    def add(self, payload):
        raise NotImplementedError

    @abstractmethod
    def delete(self, index):
        raise NotImplementedError

    @abstractmethod
    def get_one(self, index):
        raise NotImplementedError

    @abstractmethod
    def get_all(self, num_rows):
        raise NotImplementedError

    @abstractmethod
    def update(self, index, payload):
        raise NotImplementedError
