from nodeflow import func2node, Dispenser
from nodeflow.builtin import PathVariable

from src.supported_datasets import IMPLICIT_ADAPTERS
from nodeflow.converter import Converter
from pathlib import Path
from enum import Enum

from src.supported_datasets.coco.dataset import COCO_Dataset
from src.supported_datasets.coco.functions.reader import coco_reader
from src.supported_datasets.coco.functions.writer import coco_writer
from src.supported_datasets.yolo.dataset import YOLO_Dataset
from src.supported_datasets.yolo.functions.reader import yolo_reader
from src.supported_datasets.yolo.functions.writer import yolo_writer


class DatasetPath(str, Enum):
    YOLO = 'yolo'
    COCO = 'coco'


def page():
    options = [DatasetPath.YOLO, DatasetPath.COCO]

    dataset_types = {
        DatasetPath.COCO: COCO_Dataset,
        DatasetPath.YOLO: YOLO_Dataset,
    }

    readers = {
        DatasetPath.COCO: coco_reader,
        DatasetPath.YOLO: yolo_reader,
    }

    writers = {
        DatasetPath.COCO: coco_writer,
        DatasetPath.YOLO: yolo_writer,
    }
    while True:
        try:
            # Input
            print("<ctrl+c to back>")
            dataset_path = Path(input("Enter path to dataset: ")).resolve()
            if not dataset_path.exists():
                print("Could not find dataset!")
                continue

            if not dataset_path.is_dir():
                print("Dataset path should be a directory!")
                continue

            output_folder = Path(input("Enter path to empty output folder: ")).resolve()
            if output_folder.exists() and len([x for x in output_folder.iterdir()]) != 0:
                print("Folder is not empty!")
                continue

            if not dataset_path.is_dir():
                print("Output dataset path should be a directory!")
                continue

            output_folder.mkdir(parents=True, exist_ok=True)

            # Input type
            print("Select type of dataset:")
            for i, option in enumerate(options):
                print(f"{i}: {option.value}")

            idx = input('>>> ')
            if not (idx.isdigit() and int(idx) < len(options)):
                print("Invalid option. Please try again")
                continue

            input_type = options[int(idx)]

            # Target type
            print("Select target type: ")
            for i, option in enumerate(options):
                print(f"{i}: {option.value}")

            idx = input('>>> ')
            if not (idx.isdigit() and int(idx) < len(options)):
                print("Invalid option. Please try again")
                continue

            target_type = options[int(idx)]

            if input_type == target_type:
                print("Input type == Target type. There is no need to converting")
                continue

            # Converting
            Dispenser(
                dataset = Converter(IMPLICIT_ADAPTERS).convert(
                    variable = PathVariable(dataset_path) >> func2node(readers[input_type]),
                    to_type  = dataset_types[target_type],
                ),
                target_path = PathVariable(output_folder),
            ) >> func2node(writers[target_type])

        except KeyboardInterrupt:
            return

__all__ = [
    'page'
]
