from cvtk.utils.stat.iou import bbox_iou
from cvtk import Bbox


def compute_confusion_matrix(
        original_bboxes   : dict[str, list[Bbox]],
        predicted_bboxes  : dict[str, list[Bbox]],
        selected_category : int,
        threshold         : float = 0.4
) -> tuple[list[Bbox]:2, int:3]:
    filtered_original_bboxes = {}
    filtered_predicted_bboxes = {}

    total_tp = 0
    total_fp = 0
    total_fn = 0

    for image_name in original_bboxes.keys():
        filtered_original_bboxes[image_name] = filtered_original_bboxes.get(image_name, [])
        for bbox, bbox_criteria, text in original_bboxes[image_name]:
            if bbox.category != selected_category:
                continue
            filtered_original_bboxes[image_name] += [(bbox, bbox_criteria, text)]

    for image_name in predicted_bboxes.keys():
        filtered_predicted_bboxes[image_name] = []
        for predicted_bbox, bbox_criteria in predicted_bboxes[image_name]:
            if predicted_bbox.category != selected_category:
                continue
            filtered_predicted_bboxes[image_name] += [(predicted_bbox, bbox_criteria)]

    for image_name in filtered_predicted_bboxes.keys():
        classified_bboxes = set()

        tp_counter = 0
        for predicted_bbox, _ in filtered_predicted_bboxes[image_name]:
            flag = False
            flag_orig = None
            for original_bbox, _, _ in filtered_original_bboxes[image_name]:
                if bbox_iou(original_bbox, predicted_bbox) > threshold and \
                        original_bbox not in classified_bboxes and \
                        predicted_bbox not in classified_bboxes:
                    flag = True
                    flag_orig = original_bbox
                    break
            if flag:
                classified_bboxes.add(flag_orig)
                tp_counter += 1

        fp_counter = len(filtered_predicted_bboxes[image_name]) - tp_counter
        fn_counter = len(filtered_original_bboxes[image_name])  - tp_counter

        total_tp += tp_counter
        total_fp += fp_counter
        total_fn += fn_counter

    return filtered_predicted_bboxes, filtered_original_bboxes, total_tp, total_fp, total_fn


__all__ = [
    'compute_confusion_matrix'
]
