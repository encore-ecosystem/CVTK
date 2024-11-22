from pages import view
from configparser import ConfigParser
from src import PROGRAM_ROOT, print_logo


def main():
    # read config
    assert (PROGRAM_ROOT / 'config.ini').exists(), "Error: config.ini does not exist in program root, please update repo."
    config = ConfigParser()
    config.read(PROGRAM_ROOT / 'config.ini')

    print_logo(width=64)
    view()


if __name__ == '__main__':
    main()
