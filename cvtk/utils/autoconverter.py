from cvtk.supported_datasets import *
from cvtk.utils.determinator import *

from nodeflow import Converter, Variable
from pathlib import Path
from typing import Type


def autoconvert(dataset_path: Path, target_type: Type[AbstractDataset]) -> Variable:
    return Converter(
        adapters=IMPLICIT_ADAPTERS
    ).convert(
        determine_dataset(dataset_path),
        target_type
    )


__all__ = [
    'autoconvert',
]
