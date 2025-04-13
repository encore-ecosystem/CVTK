from cvtk.supported_datasets import IMPLICIT_ADAPTERS
from cvtk.utils import determine_dataset
from cvtk.interfaces import AbstractDataset
from nodeflow import Converter
from pathlib import Path
from typing import Type

def autoconvert_dataset(dataset_path: Path, target_type: Type[AbstractDataset]) -> AbstractDataset:
    return Converter(
        adapters=IMPLICIT_ADAPTERS
    ).convert(
        determine_dataset(dataset_path),
        target_type
    )


__all__ = [
    'autoconvert_dataset',
]
