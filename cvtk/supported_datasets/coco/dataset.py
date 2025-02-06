from nodeflow.builtin.variables import PathVariable
from nodeflow import Variable
from typing import Optional


class COCO_Dataset(Variable):
    def __init__(
            self,
            path: Optional[PathVariable],
            anns: dict,
            images: dict,
    ):
        super().__init__(value=path)
        self.anns   = anns
        self.images = images


__all__ = [
    'COCO_Dataset',
]
