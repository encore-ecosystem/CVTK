from pages.convert import view as view_convert
from pages.merge   import view as view_merge
from pages.filter  import view as view_filter
from pages.rename  import view as view_rename


def view():
    options = ['Merge Datasets', 'Convert Datasets', 'Rename Labels', 'Filter Labels']
    try:
        while True:
            for i, option in enumerate(options):
                print(f"{i}: {option}")

            idx = input('>>> ')
            if not (idx.isdigit() and int(idx) in range(len(options))):
                print("Invalid option.")
            idx = int(idx)

            match idx:
                case 0: view_merge()
                case 1: view_convert()
                case 2: view_rename()
                case 3: view_filter()

    except KeyboardInterrupt:
        return


__all__ = [
    'view'
]
