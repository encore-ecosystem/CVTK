from shapely.geometry import Polygon
from PIL.Image import Image
from .bbox import Bbox


class Bbox_4XY(Bbox):
    def __init__(self, points: list[float], category: int = -1, confidence: float = 0) -> None:
        assert len(points) == 8
        super().__init__(points, category, confidence)

    def area(self) -> float:
        return Polygon(zip(self.bbox[0::2], self.bbox[1::2])).area

    def get_poly(self) -> list[tuple[float, float]]:
        return list(zip(self.bbox[0::2], self.bbox[1::2]))

    def crop_on(self, image: Image) -> Image:
        return image.crop((self.bbox[0], self.bbox[1], self.bbox[2], self.bbox[3]))

    def __and__(self, other: 'Bbox_4XY') -> float:
        poly_a = Polygon(zip(self.bbox[0::2], self.bbox[1::2]))
        poly_b = Polygon(zip(other.bbox[0::2], other.bbox[1::2]))
        return poly_a.intersection(poly_b).area


__all__ = [
    'Bbox_4XY'
]
