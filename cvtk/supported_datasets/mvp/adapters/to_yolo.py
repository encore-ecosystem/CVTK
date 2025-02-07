from unittest import case

from cvtk.supported_datasets.mvp.dataset import MVP_Dataset
from cvtk.supported_datasets.yolo.dataset import YOLO_Dataset

from nodeflow import Adapter

def format_bbox(bbox_type: str, class_id: int, points: list) -> str:
    match bbox_type:
        case 'bb':
            return f"{class_id} {' '.join(map(str, points[:4]))}"
        case 'obb':
            return f"{class_id} {' '.join(map(str, points[:8]))}"
        case _:
            raise ValueError(f"Unsupported bbox_type: {bbox_type}")

class MVP2YOLO_Adapter(Adapter):
    def compute(self, variable: MVP_Dataset) -> YOLO_Dataset:
        classes = []
        anns = {split: {} for split in ['train', 'valid', 'test']}

        for split, split_data in variable.attributes.items():
            for image_path, manifest in split_data.items():
                for bbox in manifest['Detection']['bboxes']:
                    class_name = bbox['class_name']
                    if class_name not in classes:
                        classes.append(class_name)

        for split, split_data in variable.attributes.items():
            for image_path, manifest in split_data.items():
                annotations = []
                for bbox in manifest['Detection']['bboxes']:
                    class_id = classes.index(bbox['class_name'])
                    bbox_type = bbox['bbox_type']
                    points = bbox['points']
                    annotations.append(format_bbox(bbox_type, class_id, points))

                anns[split][image_path] = annotations

        return YOLO_Dataset(
            path=None,
            data_yaml={
                'train': '../train',
                'val'  : '../valid',
                'test' : '../test',
                'nc': len(classes),
                'names': classes
            },
            anns=anns,
            images=variable.images
        )

    def is_loses_information(self) -> bool:
        return True

__all__ = [
    'MVP2YOLO_Adapter'
]
