from pathlib import Path


def view():
    try:
        while True:
            #
            # Dataset path
            #
            dataset_folder_path = Path(input("Enter path to dataset folder: ")).resolve()

            if not dataset_folder_path.exists():
                print("Could not find dataset folder!")
                continue

            if not dataset_folder_path.is_dir():
                print("Datasets path should be a directory!")
                continue

            #
            # Keep ID
            #
            print("Enter labels, separated by a space!")
            labels_id = input('>>> ').strip().split()
            assert all(map(lambda s: s.isdigit(), labels_id))
            labels_id = list(map(int, labels_id))

            #
            # Logic
            #
            for split in ["train", "test", "valid"]:
                for file in (dataset_folder_path / split / "labels").glob("*.txt"):
                    with open(file, "r+") as ann_file:
                        lines = ann_file.readlines()
                        keep_lines = ""
                        for line in lines:
                            line = line.strip().split()
                            if int(line[0]) in labels_id:
                                keep_lines += f"{line[0]} " + " ".join(line[1:]) + "\n"
                        file.write_text(keep_lines)

    except KeyboardInterrupt:
        return




__all__ = [
    'view'
]
