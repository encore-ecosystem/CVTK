from cvtk.supported_datasets.abstract import AbstractDataset
from typing import Any, Optional
from pathlib import Path

import shutil
import json
import toml


class MVP_Dataset(AbstractDataset):
    def __init__(self, path: Optional[Path], manifest: dict[str, Any], images: dict[str, dict[str, Path]], attributes: dict[str, dict[str, dict[str, Any]]]):
        super().__init__(path)
        self.manifest   = manifest
        self.images     = images
        self.attributes = attributes

    @classmethod
    def is_dataset(cls, path: Path) -> bool:
        return (path / 'manifest.toml').exists()

    @classmethod
    def read(cls, path_to_dataset: Path) -> "MVP_Dataset":
        manifest_path = path_to_dataset / 'manifest.toml'
        assert manifest_path.exists(), 'Manifest file not found.'

        manifest = toml.load(manifest_path)

        images, annotations = {}, {}
        for split in ["train", "test", "valid"]:
            annotations[split], images[split] = {}, {}

            for label_file_path in (path_to_dataset / split / "attributes").glob("*.json"):
                with open(label_file_path, "rb") as label_file:
                    annotations[split][label_file_path.stem] = json.load(label_file)

            for image_file_path in (path_to_dataset / split / "images").glob("*"):
                images[split][image_file_path.stem] = image_file_path

        return MVP_Dataset(
            path=path_to_dataset,
            manifest=manifest,
            images=images,
            attributes=annotations,
        )

    def write(self, save_path: Path):
        for split in ["train", "test", "valid"]:
            (save_path / split / "attributes").mkdir(parents=True, exist_ok=True)
            (save_path / split / "images").mkdir(parents=True, exist_ok=True)

            for image_path in self.images[split].values():
                shutil.copy(
                    src=image_path,
                    dst=save_path / split / 'images' / image_path.name
                )

                with open(save_path / split / 'attributes' / f"{image_path.stem}.json", 'w') as attribute_file:
                    json.dump(self.attributes[split][f"{image_path.stem}.txt"], attribute_file, indent=4)

        with open(save_path / 'manifest.toml', "w") as manifest_file:
            manifest = {
                'Info': {
                    'source': [
                        'generated using CVTK'
                    ],
                    'version': '1.0',
                },
            }
            toml.dump(manifest, manifest_file)


__all__ = [
    "MVP_Dataset"
]
