from abc import ABCMeta, abstractmethod
from typing import Any

from PIL.Image import Image
from nodeflow import Variable


class Bbox(Variable, metaclass=ABCMeta):
    def __init__(self, bbox: list[float], value: Any, category: int = -1, confidence: float = 0):
        super().__init__(value)
        self.bbox       = list(bbox)
        self.category   = category
        self.confidence = confidence

    @abstractmethod
    def area(self) -> float:
        raise NotImplementedError

    @abstractmethod
    def get_poly(self) -> list[tuple[float, float]]:
        raise NotImplementedError

    @abstractmethod
    def crop_on(self, image: Image):
        raise NotImplementedError

    @abstractmethod
    def __and__(self, other: "Bbox") -> float:
        return NotImplemented

    def __hash__(self):
        return hash(tuple(self.bbox))

    def __eq__(self, other: 'Bbox'):
        return self.bbox == other.bbox

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.category}: {self.bbox} {self.confidence:.2f})"

    def __copy__(self):
        return self.__class__(self.bbox, self.value, self.category, self.confidence)

    def to_image_scale(self, width: int, height: int) -> 'Bbox':
        result = self.__copy__()
        for i in range(len(result.bbox)):
            result.bbox[i] *= width if i % 2 == 0 else height
        return result


__all__ = [
    'Bbox'
]
