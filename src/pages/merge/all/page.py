from pathlib import Path


def page():
    while True:
        try:
            print("<ctrl+c to back>")
            dataset_folder_path = Path(input("Enter path to datasets folder: ")).resolve()
            if not dataset_folder_path.exists():
                print("Could not find dataset folder!")

            if not dataset_folder_path.is_dir():
                print("dataset folder path should be a directory!")

        except KeyboardInterrupt:
            return


__all__ = [
    'page'
]
