from pathlib import Path
from typing import Type

from nodeflow import Converter, Variable

from .determinator import determine_dataset
from cvtk.supported_datasets import *


def autoconvert(dataset_path: Path, target_type: Type[Variable]) -> Variable:
    return Converter(
        adapters=IMPLICIT_ADAPTERS
    ).convert(
        determine_dataset(dataset_path),
        target_type
    )

__all__ = [
    'autoconvert',
]
