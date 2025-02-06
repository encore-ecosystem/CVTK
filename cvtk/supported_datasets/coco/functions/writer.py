from cvtk.supported_datasets.coco.dataset import COCO_Dataset
from nodeflow.builtin import PathVariable, Result

import shutil
import json


def coco_writer(dataset: COCO_Dataset, target_path: PathVariable) -> Result:
    root = target_path.value

    for split in ["train", "test", "valid"]:
        (root / split).mkdir(parents=True, exist_ok=True)

        for image_path in dataset.images[split].values():
            shutil.copy(
                src = image_path,
                dst = root / split / image_path.name
            )

        with open(root / split / '_annotations.json', 'w') as json_file:
            json.dump(dataset.anns[split], json_file, indent=4)

    return Result(True)


__all__ = [
    'coco_writer'
]
