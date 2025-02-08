from .abstract import *

from .coco import *
from .yolo import *
from .mvp  import *

IMPLICIT_ADAPTERS = COCO_ADAPTERS + YOLO_ADAPTERS + MVP_ADAPTERS
