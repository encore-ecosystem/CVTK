from pathlib import Path
from cvtk.supported_datasets import YOLO_Dataset, MVP_Dataset
from PIL import Image, ImageDraw

import random
import os
from cvtk.bbox import Bbox_2xy
from tqdm import tqdm

def sparce_class():
    current_dir = Path.cwd()
    datasets = os.listdir(current_dir)
    datasets = [current_dir / dataset for dataset in datasets if YOLO_Dataset.is_dataset(current_dir / dataset)]
    
    for i, dataset in enumerate(datasets):
        print(f"[{i}]: {dataset.name}")

    index = int(input(">>> "))
    if not 0 <= index <= len(datasets):
        print("Bad index")
        exit(-1)
    
    dataset = YOLO_Dataset.read(path_to_dataset=datasets[index])
    names = dataset.data_yaml["names"]
    print("names: ", names)

    sparce_rule = {}
    for name in names:
        msg = f"Convert {name} to: "
        sparce_rule[name] = input(msg)
    
    print("converting rules: ", sparce_rule)
    if not (input("Ok? y/n: ").lower() == "y"):
        exit(0)

    classes = list(set(sparce_rule.values()))
    dataset.data_yaml["nc"] = len(classes)
    dataset.data_yaml["names"] = classes

    for split in ("train", "test", "valid"):
        for key, list_value in dataset.anns[split].items():
            new_list_value = []
            for value in list_value:
                value = value.split()
                old_class = names[int(value[0])]
                value[0] = str(classes.index(sparce_rule[old_class]))
                new_list_value.append(" ".join(value))
            dataset.anns[split][key] = new_list_value
    
    output_name = input("Enter output name: ")
    dataset.write(current_dir / output_name)


def visualize_dataset():
    current_dir = Path.cwd()
    datasets = os.listdir(current_dir)
    datasets = [current_dir / dataset for dataset in datasets if MVP_Dataset.is_dataset(current_dir / dataset)]
    
    for i, dataset in enumerate(datasets):
        print(f"[{i}]: {dataset.name}")

    index = int(input(">>> "))
    if not 0 <= index <= len(datasets):
        print("Bad index")
        exit(-1)
    
    dataset = MVP_Dataset.read(path_to_dataset=datasets[index])
    
    output_name = input("Enter output name: ")
    output_path = current_dir / output_name
    output_path.mkdir()
    for split in tqdm(("train", "test", "valid")):
        split_path = output_path / split
        split_path.mkdir()
        for image_stem in tqdm(dataset.images[split]):
            image_path = dataset.images[split][image_stem]
            image_attr = dataset.attributes[split][image_stem]

            image = Image.open(image_path)
            d = ImageDraw.Draw(image)
            for bbox in image_attr["Detection"]["bboxes"]:
                bbox_xy = Bbox_2xy(points = bbox["points"], value = bbox["class_name"])
                scaled = bbox_xy.to_image_scale(image.width, image.height)
                d.rectangle(scaled.bbox, width=3)
                d.text((scaled.bbox[0], scaled.bbox[1]), text=bbox_xy.value)
            image.save(split_path / image_path.name)


def shrink_dataset():
    current_dir = Path.cwd()
    datasets = os.listdir(current_dir)
    datasets = [current_dir / dataset for dataset in datasets if YOLO_Dataset.is_dataset(current_dir / dataset)]
    
    for i, dataset in enumerate(datasets):
        print(f"[{i}]: {dataset.name}")

    index = int(input(">>> "))
    if not 0 <= index <= len(datasets):
        print("Bad index")
        exit(-1)
    
    dataset = YOLO_Dataset.read(path_to_dataset=datasets[index])
    
    output_name = input("Enter output name: ")
    output_path = current_dir / output_name
    output_path.mkdir()
    
    split = input("enter target split (train, test or valid): ")
    assert split in ("train", "test", "valid")
    
    target_count = int(input("enter target count: "))
    assert target_count >= 0

    split_path = output_path / split
    split_path.mkdir()
    
    all_images = list(dataset.images[split].keys())
    if len(all_images) < target_count:
        print(f"There no images to remove! target={target_count} but dataset have {len(all_images)}")
        exit(1)

    sparced_images = random.choices(all_images, k=target_count)
    saved_images = {}
    saved_anns = {}
    for image_stem in tqdm(sparced_images):
        saved_images[image_stem] = dataset.images[split][image_stem]
        saved_anns[f"{image_stem}.txt"] = dataset.anns[split][f"{image_stem}.txt"]

    dataset.images[split] = saved_images
    dataset.anns[split]   = saved_anns
    
    dataset.write(output_path)    


def entrypoint():
    print("0: Sparce Yolo Dataset Classes")
    print("1: Visualize MVP Dataset")
    print("2: Shirnk split of Yolo Dataset")

    menu = int(input(">>> "))
    match menu:
        case 0:
            sparce_class()
        case 1:
            visualize_dataset()
        case 2:
            shrink_dataset()
        case _:
            print("Unknown mode")
            exit(-1)
