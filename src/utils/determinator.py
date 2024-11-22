from nodeflow.builtin import PathVariable
from pathlib import Path
from src.supported_datasets import yolo_reader, coco_reader


def determine_dataset(dataset_path: Path):
    if (dataset_path / 'data.yaml').exists():
        return yolo_reader(PathVariable(dataset_path))
    else:
        return coco_reader(PathVariable(dataset_path))


__all__ = ['determine_dataset']
