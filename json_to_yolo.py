from pathlib import Path
import json
import shutil

# Path to COCO
image_directory = Path().resolve() / "datasets" / "COCO"

# Output path
output_base_directory = Path().resolve() / "datasets" / "YOLO"

for split in ["train", "valid", "test"]:
    split_path = image_directory / split
    output_directory = output_base_directory / split

    if output_directory.exists():
        shutil.rmtree(output_directory)
    output_directory.mkdir(parents=True, exist_ok=True)

    (output_directory / "images").mkdir(exist_ok=True)
    (output_directory / "labels").mkdir(exist_ok=True)

    coco_json_path = list(split_path.glob("*.json"))
    if not coco_json_path:
        print(f"Файл JSON не найден для раздела {split}")
        continue

    with open(coco_json_path[0], "r", encoding="utf-8") as f:
        coco_data = json.load(f)

    category_mapping = {cat["id"]: cat["name"] for cat in coco_data["categories"]}
    category_id_mapping = {cat["name"]: cat["id"] for cat in coco_data["categories"]}

    for image in coco_data["images"]:
        image_id = image["id"]
        file_name = image["file_name"]
        source_image_path = split_path / file_name

        if source_image_path.exists():
            shutil.copy(source_image_path, output_directory / "images" / file_name)

        label_file_path = output_directory / "labels" / f"{file_name.replace('.jpg', '.txt')}"

        with open(label_file_path, "w") as label_file:
            for annotation in coco_data["annotations"]:
                if annotation["image_id"] == image_id:
                    x_center = (annotation["bbox"][0] + annotation["bbox"][2] / 2) / image["width"]
                    y_center = (annotation["bbox"][1] + annotation["bbox"][3] / 2) / image["height"]
                    width = annotation["bbox"][2] / image["width"]
                    height = annotation["bbox"][3] / image["height"]

                    category_id = category_id_mapping[category_mapping[annotation["category_id"]]]
                    label_file.write(f"{category_id - 1} {x_center} {y_center} {width} {height}\n")

print("Конвертация завершена!")