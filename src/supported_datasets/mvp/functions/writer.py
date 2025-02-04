from src.supported_datasets.mvp.dataset import MVP_Dataset
from nodeflow.builtin import PathVariable, Result

import shutil
import json
import toml

def mvp_writer(dataset: MVP_Dataset, dataset_path: PathVariable) -> Result:
    # create directories
    for split in ["train", "test", "valid"]:
        (dataset_path / split / "attributes").mkdir(parents=True, exist_ok=True)
        (dataset_path / split / "images").mkdir(parents=True, exist_ok=True)

        for image_path in dataset.images[split].values():
            shutil.copy(
                src = image_path,
                dst = dataset_path / split / 'images' / image_path.name
            )

            with open(dataset_path / split / 'attributes' / f"{image_path.stem}.json", 'w') as attribute_file:
                json.dump(dataset.attributes[split][f"{image_path.stem}.txt"], attribute_file, indent=4)

    with open(dataset_path / 'manifest.toml', "w") as manifest_file:
        manifest = {
            'Info': {
                'source' : [
                    'generated using CVTK'
                ],
                'version': '1.0',
            },
        }
        toml.dump(manifest, manifest_file)

    return Result(True)


__all__ = [
    'mvp_writer'
]
