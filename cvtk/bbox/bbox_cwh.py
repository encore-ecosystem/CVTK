from shapely.geometry import Polygon, box
from cvtk.bbox.bbox_2xy import Bbox_2xy
from PIL.Image import Image
from .bbox import Bbox


class Bbox_CWH(Bbox):
    def __init__(self, points: list[float], category: int = -1, confidence: float = 0):
        assert len(points) == 4
        super().__init__(points, category, confidence)

    def area(self) -> float:
        return self.bbox[2] * self.bbox[3]

    def get_shapely_polygon(self) -> Polygon:
        return Polygon([
            (self.bbox[0] - self.bbox[2] / 2, self.bbox[1] - self.bbox[3] / 2),
            (self.bbox[0] + self.bbox[2] / 2, self.bbox[1] - self.bbox[3] / 2),
            (self.bbox[0] + self.bbox[2] / 2, self.bbox[1] + self.bbox[3] / 2),
            (self.bbox[0] - self.bbox[2] / 2, self.bbox[1] + self.bbox[3] / 2),
        ])

    def get_poly(self) -> list[tuple[float, float]]:
        return list(self.get_shapely_polygon().exterior.coords)

    def crop_on(self, image: Image):
        raise NotImplementedError()

    def __and__(self, other: 'Bbox_CWH') -> float:
        if isinstance(other, Bbox_CWH):
            return self.get_shapely_polygon().intersection(other.get_shapely_polygon()).area
        elif isinstance(other, Bbox_2xy):
            return self.get_shapely_polygon().intersection(box(*other.bbox)).area
        raise NotImplementedError(f"Unknown type {type(other)}")


__all__ = [
    'Bbox_CWH'
]
