from abc import ABCMeta, abstractmethod
from nodeflow import Variable
from pathlib import Path


class AbstractDataset(Variable, metaclass=ABCMeta):
    def __init__(self, path: Path):
        super().__init__(path)

    @classmethod
    @abstractmethod
    def is_dataset(cls, path: Path) -> bool:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def read(cls, path_to_dataset: Path) -> 'AbstractDataset':
        raise NotImplementedError

    @abstractmethod
    def write(self, save_path: Path):
        raise NotImplementedError


__all__ = [
    'AbstractDataset',
]
