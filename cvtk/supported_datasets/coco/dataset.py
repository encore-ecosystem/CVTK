from cvtk.supported_datasets.abstract import AbstractDataset
from typing import Optional
from pathlib import Path

import shutil
import json


class COCO_Dataset(AbstractDataset):
    def __init__(self, path: Optional[Path], anns: dict, images: dict):
        super().__init__(path)
        self.anns   = anns
        self.images = images

    @classmethod
    def is_dataset(cls, path: Path) -> bool:
        return all([
            (path / split / '_annotations.json').exists() for split in ['train', 'valid', 'test']
        ])

    @classmethod
    def read(cls, path_to_dataset: Path) -> 'AbstractDataset':
        annotations, images = {}, {}
        for split in ["train", "test", "valid"]:
            annotations[split], images[split] = {}, {}

            shrinkage_superclass_mapping = {}
            all_categories_mapping = {}
            assert (path_to_dataset / split / "_annotations.json").exists()
            with open(path_to_dataset / split / "_annotations.json", "r") as f:
                data = json.load(f)
                for category in data["categories"]:
                    all_categories_mapping[category["id"]] = category["name"]
                    shrinkage_superclass_mapping[category["name"]] = shrinkage_superclass_mapping.get(
                        category["name"], []
                    ) + [category["id"]]

                for category in data["annotations"]:
                    category['category_id'] = min(
                        shrinkage_superclass_mapping[all_categories_mapping[category['category_id']]])

                data['categories'] = [
                    {
                        'id': min(shrinkage_superclass_mapping[category]),
                        'name': category,
                        'supercategory': 'none'
                    }
                    for category in shrinkage_superclass_mapping
                ]
                annotations[split] = data

            images_directory = path_to_dataset / split
            for image_file_path in images_directory.iterdir():
                if image_file_path.suffix in ['.jpg', '.jpeg', '.png']:
                    images[split][image_file_path.stem] = image_file_path / image_file_path

        return COCO_Dataset(path=path_to_dataset, anns=annotations, images=images)

    def write(self, save_path: Path):
        for split in ["train", "test", "valid"]:
            (save_path / split).mkdir(parents=True, exist_ok=True)

            for image_path in self.images[split].values():
                shutil.copy(
                    src = image_path,
                    dst = save_path / split / image_path.name
                )

            with open(save_path / split / '_annotations.json', 'w') as json_file:
                json.dump(self.anns[split], json_file, indent=4)


__all__ = [
    'COCO_Dataset',
]
