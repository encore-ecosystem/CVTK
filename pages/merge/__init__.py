from functools import reduce
from nodeflow import Converter, Dispenser
from nodeflow.builtin import PathVariable

from src.utils import determine_dataset
from pathlib import Path
import os
from src.supported_datasets import IMPLICIT_ADAPTERS, yolo_writer, coco_writer
from src.utils import combine_coco_datasets


def view():
    try:
        while True:
            #
            # Input
            #
            dataset_folder_path = Path(input("Enter path to datasets folder: ")).resolve()

            if not dataset_folder_path.exists():
                print("Could not find datasets folder!")
                continue

            if not dataset_folder_path.is_dir():
                print("Datasets folder path should be a directory!")
                continue
            #
            # Output
            #
            output_folder_path = Path(input("Enter path to output folder: ")).resolve()
            output_folder_path.mkdir(parents=True, exist_ok=True)
            if not os.listdir(output_folder_path):
                print("Output folder path should be empty!")
                continue

            #
            # Dataset type
            #
            options = ['YOLO', 'COCO']
            print("Select type of result dataset:")
            for i, option in enumerate(options):
                print(f"{i}: {option}")

            idx = input('>>> ')
            if not (idx.isdigit() and int(idx) in range(len(options))):
                print("Invalid option. Please try again")
                continue

            input_type = options[int(idx)]

            #
            # Combine
            #
            datasets = [name for name in os.listdir(dataset_folder_path)]
            for i, name in enumerate(datasets):
                print(f"{i}. {name}")
            print('choose datasets index, separated by comma')
            indexes = list(map(lambda s: int(s.strip()), input(">>> ").split(',')))
            assert all(idx in range(len(datasets)) for idx in indexes)

            datasets = list(
                map(
                    lambda index: determine_dataset(
                        dataset_folder_path / datasets[index],
                    ), indexes)
            )

            with Converter(adapters=IMPLICIT_ADAPTERS):
                Dispenser(
                    dataset     = reduce(combine_coco_datasets, datasets),
                    target_path = PathVariable(output_folder_path),
                ) >> {'YOLO': yolo_writer, 'COCO': coco_writer}[input_type]

    except KeyboardInterrupt:
        return


__all__ = [
    'view'
]
