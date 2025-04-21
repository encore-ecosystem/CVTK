from nodeflow import Adapter

from cvtk.bbox.bboxes.bbox_2xy import Bbox_2xy
from cvtk.bbox.bboxes.bbox_cwh import Bbox_CWH


class Adapter2xyCwh(Adapter):
    def compute(self, variable: Bbox_2xy) -> Bbox_CWH:
        lx, ly, rx, ry = variable.bbox
        cx = (lx + rx) / 2
        cy = (ly + ry) / 2
        w = rx - lx
        h = ry - ly
        return Bbox_CWH(
            points     = [cx, cy, w, h],
            value      = variable.value,
            category   = variable.category,
            confidence = variable.confidence,
        )

    def is_loses_information(self) -> bool:
        return False


__all__ = [
    "Adapter2xyCwh"
]
