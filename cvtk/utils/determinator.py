from cvtk.supported_datasets import YOLO_Dataset, COCO_Dataset, MVP_Dataset
from cvtk import AbstractDataset
from pathlib import Path


def determine_dataset(dataset_path: Path) -> AbstractDataset:
    datasets = [YOLO_Dataset, MVP_Dataset, COCO_Dataset]

    for dataset in datasets:
        if dataset.is_dataset(dataset_path):
            return dataset.read(dataset_path)

    raise ValueError("Dataset not found")


__all__ = [
    'determine_dataset'
]
