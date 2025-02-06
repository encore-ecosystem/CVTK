from unittest import case

from cvtk.supported_datasets.mvp.dataset import MVP_Dataset
from cvtk.supported_datasets.yolo.dataset import YOLO_Dataset

from nodeflow import Adapter

def determine_bbox_type(line: str) -> str:
    seps = line.split()
    match len(seps):
        case 5:
            return 'bb'
        case 9:
            return 'obb'
        case _:
            return 'null'

class YOLO2MVP_Adapter(Adapter):
    def compute(self, variable: YOLO_Dataset) -> MVP_Dataset:
        classes = variable.data_yaml['names']

        attributes = {}
        for split in ['train', 'valid', 'test']:
            attributes[split] = {}
            for image_path in variable.anns[split]:
                manifest = {
                    'Detection': {
                        'bboxes': [
                            {
                                'superclasses': [],
                                'bbox_type'   : determine_bbox_type(line),
                                'class_name'  : classes[int(line.split()[0])],
                                'points'      : list(map(float, line.split()[1:])),
                                'recognition_text' : None,

                            } for line in variable.anns[split][image_path]
                        ],
                        'keypoints': [],
                    },

                    'Segmentation': {
                        'polygons': [
                            [],
                        ],
                    }
                }
                attributes[split][image_path] = manifest

        return MVP_Dataset(
            path=None,
            manifest={'version': '1.0', 'source': ['generated using CVTK from YOLO']},
            images=variable.images,
            attributes=attributes,
        )

    def is_loses_information(self) -> bool:
        return False


__all__ = [
    'YOLO2MVP_Adapter'
]
