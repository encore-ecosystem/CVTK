import os


def clear_terminal():
    # deprecated
    # os.system('cls' if os.name == 'nt' else 'clear')
    pass

def print_logo(width: int, border_char: str = '#', empty_char: str = ' '):
    assert len(empty_char) == 1, "Empty char should only be one character"
    logo = """
 ██████╗██╗   ██╗████████╗██╗  ██╗
██╔════╝██║   ██║╚══██╔══╝██║ ██╔╝
██║     ██║   ██║   ██║   █████╔╝ 
██║     ╚██╗ ██╔╝   ██║   ██╔═██╗ 
╚██████╗ ╚████╔╝    ██║   ██║  ██╗
 ╚═════╝  ╚═══╝     ╚═╝   ╚═╝  ╚═╝
by Encore Ecosystem
"""
    print(border_char * width)
    for line in logo.splitlines():
        print(border_char + f"{line:{empty_char}^{width - 2}}" + border_char)
    print(border_char * width)

__all__ = [
    'clear_terminal',
    'print_logo',
]
