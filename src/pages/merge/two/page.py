from typing import Optional
from pathlib import Path
import time


def get_dataset_path(hint: str) -> Optional[Path]:
    dataset_path = Path(input(f"{hint} dataset path: ")).resolve()
    if not dataset_path.exists():
        print("Dataset path does not exist!")
        time.sleep(2)
        return
    if not dataset_path.is_dir():
        print("Dataset path is not a directory!")
        time.sleep(2)
        return

    return dataset_path


def page():
    while True:
        try:
            print("<ctrl+c to back>")
            first_dataset_path = get_dataset_path("First")
            if first_dataset_path is None:
                return
            second_dataset_path = get_dataset_path("Second")
            if second_dataset_path is None:
                return

        except KeyboardInterrupt:
            return


__all__ = [
    'page'
]
