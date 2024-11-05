from src.terminal import clear_terminal
from src.pages.merge.two.page import page as merge_two
from src.pages.merge.all.page import page as merge_all
from enum import Enum
import time


class MargeMenuOptions(str, Enum):
    TWO  = "Merge 2 datasets"
    ALL  = "Merge all Dataset in folder"
    BACK = "Back"


def page():
    options = [MargeMenuOptions.TWO, MargeMenuOptions.ALL, MargeMenuOptions.BACK]

    while True:
        # print options
        for i, option in enumerate(options):
            print(f"{i}: {option.value}")

        idx = input('>>> ')
        if not (idx.isdigit() and int(idx) < len(options)):
            print("Invalid option. Please try again in 2 seconds.")
            time.sleep(2)
            return

        match options[int(idx)]:

            case MargeMenuOptions.TWO:
                merge_two()

            case MargeMenuOptions.ALL:
                merge_all()

            case MargeMenuOptions.BACK:
                clear_terminal()
                return


__all__ = [
    'page'
]
