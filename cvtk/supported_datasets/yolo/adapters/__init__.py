from .to_coco import *
from .to_mvp import *

YOLO_ADAPTERS = [
    YOLO2COCO_Adapter(),
    YOLO2MVP_Adapter(),
]
