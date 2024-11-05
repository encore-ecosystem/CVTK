from src.pages.convert.page import page as convert_page
from src.pages.merge.page import page as merge_page
from src.terminal import clear_terminal, print_logo

from enum import Enum

import time


class MainMenuOption(str, Enum):
    MERGE   = "Merge Datasets"
    CONVERT = "Convert Dataset"
    EXIT    = "Exit"


def page():
    options = [MainMenuOption.MERGE, MainMenuOption.CONVERT, MainMenuOption.EXIT]

    while True:
        clear_terminal()

        for i, option in enumerate(options):
            print(f"{i}: {option.value}")

        idx = input('>>> ')
        if not (idx.isdigit() and int(idx) < len(options)):
            print("Invalid option. Please try again in 2 seconds.")
            time.sleep(2)
            return



        match options[int(idx)]:

            case MainMenuOption.MERGE:
                merge_page()

            case MainMenuOption.CONVERT:
                convert_page()

            case MainMenuOption.EXIT:
                clear_terminal()
                break

__all__ = ["page"]
