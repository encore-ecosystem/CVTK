from nodeflow import Dispenser
from nodeflow.builtin import PathVariable

from src.supported_datasets import IMPLICIT_ADAPTERS
from nodeflow.converter import Converter
from pathlib import Path
from src.supported_datasets.coco.dataset import COCO_Dataset
from src.supported_datasets.coco.functions.reader import coco_reader
from src.supported_datasets.coco.functions.writer import coco_writer
from src.supported_datasets.yolo.dataset import YOLO_Dataset
from src.supported_datasets.yolo.functions.reader import yolo_reader
from src.supported_datasets.yolo.functions.writer import yolo_writer


def view():
    options = ['YOLO', 'COCO']

    dataset_types = {
        'YOLO' : YOLO_Dataset,
        'COCO' : COCO_Dataset,
    }

    readers = {
        'YOLO' : yolo_reader,
        'COCO' : coco_reader,
    }

    writers = {
        'YOLO' : yolo_writer,
        'COCO' : coco_writer,
    }
    while True:
        try:
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
                print(f"{i}: {option}")

            idx = input('>>> ')
            if not (idx.isdigit() and int(idx) in range(len(options))):
                print("Invalid option. Please try again")
                continue

            input_type = options[int(idx)]

            # Target type
            print("Select target type: ")
            for i, option in enumerate(options):
                print(f"{i}: {option}")

            idx = input('>>> ')
            if not (idx.isdigit() and int(idx) in range(len(options))):
                print("Invalid option. Please try again")
                continue

            target_type = options[int(idx)]

            if input_type == target_type:
                print("Input type == Target type. There is no need to converting")
                continue

            # Converting
            with Converter(IMPLICIT_ADAPTERS):
                Dispenser(
                    dataset     = PathVariable(dataset_path) >> readers[input_type],
                    target_path = PathVariable(output_folder),
                ) >> writers[target_type]

        except KeyboardInterrupt:
            return


__all__ = [
    'view'
]
