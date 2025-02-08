from cvtk.supported_datasets.abstract import AbstractDataset
from typing import Optional, Any
from pathlib import Path

import shutil
import yaml


class YOLO_Dataset(AbstractDataset):
    def __init__(self, path: Optional[Path], data_yaml: Any, anns: dict[str, Any], images: dict[str, Any]):
        super().__init__(path)
        self.data_yaml = data_yaml
        self.anns      = anns
        self.images    = images

    @classmethod
    def is_dataset(cls, path: Path) -> bool:
        return (path / 'data.yaml').exists()

    @classmethod
    def read(cls, path_to_dataset: Path) -> 'YOLO_Dataset':
        data_yaml_path = path_to_dataset / 'data.yaml'
        assert data_yaml_path.exists(), "Could not find .yaml file"

        with open(data_yaml_path, "r") as data_yaml_file:
            data_yaml = yaml.load(data_yaml_file, Loader=yaml.SafeLoader)

        annotations, images = {}, {}
        for split in ["train", "test", "valid"]:
            annotations[split], images[split] = {}, {}

            path_ = path_to_dataset / split / "labels"
            for label_file_path in path_.glob("*.txt"):
                with open(label_file_path, "r") as label_file:
                    annotations[split][label_file_path.name] = label_file.readlines()

            images_directory = path_to_dataset / split / "images"
            for image_file_path in images_directory.iterdir():
                images[split][image_file_path.stem] = images_directory / image_file_path

        return YOLO_Dataset(
            path=path_to_dataset,
            data_yaml=data_yaml,
            anns=annotations,
            images=images,
        )

    def write(self, save_path: Path):
        for split in ["train", "test", "valid"]:
            (save_path / split / "labels").mkdir(parents=True, exist_ok=True)
            (save_path / split / "images").mkdir(parents=True, exist_ok=True)

            for image_path in self.images[split].values():
                shutil.copy(
                    src = image_path,
                    dst = save_path / split / 'images' / image_path.name
                )

                with open(save_path / split / 'labels' / f"{image_path.stem}.txt", 'w') as label_file:
                    anns_str = self.anns[split][image_path.stem].__str__()[2:-2].replace("'", '').replace(', ', '\n')
                    label_file.write(anns_str)

        with open(save_path / 'data.yaml', "w") as yaml_file:
            data_yaml = {
                'train' : self.data_yaml['train'],
                'val'   : self.data_yaml['val'],
                'test'  : self.data_yaml['test'],
                'nc'    : self.data_yaml['nc'],
                'names' : self.data_yaml['names'],
            }
            yaml.dump(data_yaml, yaml_file)


__all__ = [
    'YOLO_Dataset',
]
