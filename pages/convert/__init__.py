from nodeflow import Dispenser
from nodeflow.builtin import PathVariable
from nodeflow import func2node

from cvtk.supported_datasets import IMPLICIT_ADAPTERS, YOLO2MVP_Adapter
from nodeflow.converter import Converter
from pathlib import Path
from cvtk.supported_datasets.coco.dataset import COCO_Dataset
from cvtk.supported_datasets.coco.functions.reader import coco_reader
from cvtk.supported_datasets.coco.functions.writer import coco_writer
from cvtk.supported_datasets.mvp import MVP_Dataset, mvp_reader, mvp_writer
from cvtk.supported_datasets.yolo.dataset import YOLO_Dataset
from cvtk.supported_datasets.yolo.functions.reader import yolo_reader
from cvtk.supported_datasets.yolo.functions.writer import yolo_writer


def view():
    dataset_path = Path(r'C:\Users\Kotto\Desktop\target_pictures')
    output_folder = Path(r'C:\Users\Kotto\Desktop\result')

    a = yolo_reader(PathVariable(dataset_path))
    b = YOLO2MVP_Adapter().compute(a)
    mvp_writer(b, PathVariable(output_folder))

    # options = ['YOLO', 'COCO', 'MVP']
    #
    # dataset_types = {
    #     'YOLO' : YOLO_Dataset,
    #     'COCO' : COCO_Dataset,
    #     'MVP'  : MVP_Dataset,
    # }
    #
    # readers = {
    #     'YOLO' : yolo_reader,
    #     'COCO' : coco_reader,
    #     'MVP'  : mvp_reader,
    # }
    #
    # writers = {
    #     'YOLO' : yolo_writer,
    #     'COCO' : coco_writer,
    #     'MVP'  : mvp_writer,
    # }
    # while True:
    #     try:
    #         # dataset_path = Path(input("Enter path to dataset: ")).resolve()
    #         dataset_path = Path(r'C:\Users\Kotto\Desktop\target_pictures')
    #         if not dataset_path.exists():
    #             print("Could not find dataset!")
    #             continue
    #
    #         if not dataset_path.is_dir():
    #             print("Dataset path should be a directory!")
    #             continue
    #
    #         # output_folder = Path(input("Enter path to empty output folder: ")).resolve()
    #         output_folder = Path(r'C:\Users\Kotto\Desktop\result')
    #         # if output_folder.exists() and len([x for x in output_folder.iterdir()]) != 0:
    #         #     print("Folder is not empty!")
    #         #     continue
    #
    #         if not dataset_path.is_dir():
    #             print("Output dataset path should be a directory!")
    #             continue
    #
    #         output_folder.mkdir(parents=True, exist_ok=True)
    #
    #         # Input type
    #         print("Select type of dataset:")
    #         for i, option in enumerate(options):
    #             print(f"{i}: {option}")
    #
    #         idx = input('>>> ')
    #         if not (idx.isdigit() and int(idx) in range(len(options))):
    #             print("Invalid option. Please try again")
    #             continue
    #
    #         input_type = options[int(idx)]
    #
    #         # Target type
    #         print("Select target type: ")
    #         for i, option in enumerate(options):
    #             print(f"{i}: {option}")
    #
    #         idx = input('>>> ')
    #         if not (idx.isdigit() and int(idx) in range(len(options))):
    #             print("Invalid option. Please try again")
    #             continue
    #
    #         target_type = options[int(idx)]
    #
    #         if input_type == target_type:
    #             print("Input type == Target type. There is no need to converting")
    #             continue
    #
    #         # Converting
    #         with Converter(IMPLICIT_ADAPTERS):
    #             Dispenser(
    #                 dataset      = PathVariable(dataset_path) >> func2node(readers[input_type]),
    #                 dataset_path = PathVariable(output_folder),
    #             ) >> func2node(writers[target_type])
    #
    #         print("Ready!")
    #
    #     except KeyboardInterrupt:
    #         return


__all__ = [
    'view'
]
