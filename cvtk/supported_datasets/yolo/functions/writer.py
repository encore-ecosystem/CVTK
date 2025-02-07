from cvtk.supported_datasets.yolo.dataset import YOLO_Dataset
from nodeflow.builtin import PathVariable, Result

import shutil
import yaml


def yolo_writer(dataset: YOLO_Dataset, target_path: PathVariable) -> Result:
    root = target_path.value

    # create directories
    for split in ["train", "test", "valid"]:
        (root / split / "labels").mkdir(parents=True, exist_ok=True)
        (root / split / "images").mkdir(parents=True, exist_ok=True)

        for image_path in dataset.images[split].values():
            shutil.copy(
                src = image_path,
                dst = root / split / 'images' / image_path.name
            )

            with open(root / split / 'labels' / f"{image_path.stem}.txt", 'w') as label_file:
                anns_str = dataset.anns[split][image_path.stem].__str__()[2:-2].replace("'", '').replace(', ', '\n')
                label_file.write(anns_str)

    with open(root / 'data.yaml', "w") as yaml_file:
        data_yaml = {
            'train': dataset.data_yaml['train'],
            'val'  : dataset.data_yaml['val'],
            'test' : dataset.data_yaml['test'],
            'nc'   : dataset.data_yaml['nc'],
            'names': dataset.data_yaml['names'],
        }
        yaml.dump(data_yaml, yaml_file)

    return Result(True)


__all__ = [
    'yolo_writer'
]
