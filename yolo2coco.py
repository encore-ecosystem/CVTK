import cv2
from pathlib import Path
import json
import shutil
from tqdm import tqdm
import yaml

FILE_FORMAT = ".png"
START_IDX = 0

yolo_directory = Path().resolve() / "datasets" / "YOLO"
coco_output_directory = Path().resolve() / "datasets" / "COCO"

categories = []
dataset_file_path = yolo_directory / "dataset.yaml"

with open(dataset_file_path, "r") as dataset_file:
    data = yaml.load(dataset_file, Loader=yaml.SafeLoader)
    cat_names = data["names"]
    categories = [{"id": id, "name": cat_name} for id, cat_name in enumerate(cat_names, start=START_IDX)]

category_mapping = {cat["id"]: cat["name"] for cat in categories}
category_id_mapping = {cat["name"]: cat["id"] for cat in categories}

coco_data = {
    "images": [],
    "annotations": [],
    "categories": categories,
}

for split in ["train", "valid", "test"]:
    split_path = yolo_directory / split
    images_path = split_path / "images"
    labels_path = split_path / "labels"

    if not images_path.exists() or not labels_path.exists():
        print(f"Could not find YOLO {split} images and labels")
        continue

    if not any(Path(images_path).iterdir()) or not any(Path(labels_path).iterdir()):
        print("Annotation and image folders are empty!")
        continue

    output_directory = coco_output_directory / split

    if output_directory.exists():
        shutil.rmtree(output_directory)
    output_directory.mkdir(parents=True, exist_ok=True)

    output_json_path = output_directory / "_annotations.json"
    output_json_path.parent.mkdir(parents=True, exist_ok=True)

    image_id = START_IDX
    annotation_id = START_IDX
    print(f"Started converting {split} images")
    for image_file in tqdm(list(images_path.glob(f"*{FILE_FORMAT}"))):
        label_file_path = labels_path / f"{image_file.stem}.txt"
        if not label_file_path.exists():
            print(f"Could not find {split} annotation file for {image_file}")
            continue

        im = cv2.imread(images_path / image_file)
        height, width, _ = im.shape
        
        image_info = {
            "id": image_id,
            "file_name": image_file.name,
            "width": width,
            "height": height,
        }
        coco_data["images"].append(image_info)

        shutil.copy(image_file, output_directory / image_file.name)

        with open(label_file_path, "r") as label_file:
            for line in label_file:
                class_id, x_center, y_center, width, height = map(float, line.split())
                
                x_min = int((x_center - width / 2) * image_info["width"])
                y_min = int((y_center - height / 2) * image_info["height"])
                bbox_width = int(width * image_info["width"])
                bbox_height = int(height * image_info["height"])

                annotation = {
                    "id": annotation_id,
                    "image_id": image_id,
                    "category_id": int(class_id),
                    "bbox": [x_min, y_min, bbox_width, bbox_height],
                    "area": bbox_width * bbox_height,
                    "iscrowd": 0,
                }
                coco_data["annotations"].append(annotation)
                annotation_id += 1

        image_id += 1

    with open(output_json_path, "w") as f:
        json.dump(coco_data, f, indent=4)

    coco_data["images"] = []
    coco_data["annotations"] = []

print("Done!")