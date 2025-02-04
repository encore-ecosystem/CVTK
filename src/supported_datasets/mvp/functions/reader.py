from src.supported_datasets.mvp.dataset import MVP_Dataset
from nodeflow.builtin import PathVariable
import tomllib


def mvp_reader(path_to_dataset: PathVariable) -> MVP_Dataset:
    manifest_path = path_to_dataset / 'manifest.toml'
    assert manifest_path.exists(), "Manifest file not found."

    with open(manifest_path, 'rb') as f:
        manifest = tomllib.load(f)

    images, annotations = {}, {}
    for split in ["train", "test", "valid"]:
        annotations[split], images[split] = {}, {}

        for label_file_path in (path_to_dataset / split / "attributes").glob("*.toml"):
            with open(label_file_path, "rb") as label_file:
                annotations[split][label_file_path.stem] = tomllib.load(label_file)

        for image_file_path in (path_to_dataset / split / "images").glob("*"):
            images[split][image_file_path.stem] = image_file_path

    return MVP_Dataset(
        path=path_to_dataset,
        manifest=manifest,
        images=images,
        attributes=annotations,
    )


__all__ = [
    'mvp_reader',
]
