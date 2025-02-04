from nodeflow.builtin.variables import PathVariable
from nodeflow import Variable
from pathlib import Path
from typing import Any, Optional


class MVP_Dataset(Variable):
    def __init__(self, path: Optional[PathVariable], manifest: dict[str, Any], images: dict[str, dict[str, Path]], attributes: dict[str, dict[str, dict[str, Any]]]):
        super().__init__(path)
        self.manifest = manifest
        self.images = images
        self.attributes = attributes


__all__ = [
    "MVP_Dataset"
]
