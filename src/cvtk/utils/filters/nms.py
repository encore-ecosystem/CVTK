from src.cvtk import bbox_iou
from src.cvtk.interfaces import Bbox


def nms(bboxes: list[Bbox], iou_threshold: float) -> list[Bbox]:
    result_bboxes = set(bboxes)
    for bbox_a in bboxes:
        to_delete = set()
        for bbox_b in result_bboxes - {bbox_a}:
            if bbox_a.category == bbox_b.category and bbox_iou(bbox_a, bbox_b) > iou_threshold:
                if bbox_a.confidence < bbox_b.confidence:
                    to_delete.add(bbox_a)
                else:
                    to_delete.add(bbox_b)
        result_bboxes -= to_delete
    return list(result_bboxes)


__all__ = [
    'nms'
]
