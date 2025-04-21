from nodeflow import Adapter

from cvtk.bbox.bboxes.bbox_2xy import Bbox_2xy
from cvtk.bbox.bboxes.bbox_cwh import Bbox_CWH


class AdapterCwh2xy(Adapter):
    def compute(self, variable: Bbox_CWH) -> Bbox_2xy:
        cx, cy, w, h = variable.bbox
        lx = cx - w / 2
        ly = cy - h / 2
        rx = cx + w / 2
        ry = cy + h / 2
        return Bbox_2xy(
            points     = [lx, ly, rx, ry],
            category   = variable.category,
            value      = variable.value,
            confidence = variable.confidence,
        )

    def is_loses_information(self) -> bool:
        return False


__all__ = [
    "AdapterCwh2xy"
]
