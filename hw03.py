
import sys
from pathlib import Path
from colorama import init, Fore, Style

# Ініціалізація colorama
init(autoreset=True)
# path = Path("/Users/user/Probe/venv/hw03.py")

def print_directory_tree(path: Path, prefix=""):
    if not path.is_dir():
        return

    items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
    for index, item in enumerate(items):
        connector = "┗━ " if index == len(items) - 1 else "┣━ "

        if item.is_dir():
            print(f"{prefix}{Fore.BLUE}{connector}{item.name}{Style.RESET_ALL}")
            extension = "    " if index == len(items) - 1 else "┃   "
            print_directory_tree(item, prefix + extension)
        else:
            print(f"{prefix}{Fore.GREEN}{connector}{item.name}{Style.RESET_ALL}")

def main():
    if len(sys.argv) < 2:
        print(Fore.RED + "❌ Помилка: Не вказано шлях до директорії." + Style.RESET_ALL)
        print("Приклад використання: python hw03.py /шлях/до/директорії")
        sys.exit(1)

    dir_path = Path(sys.argv[1])

    if not dir_path.exists():
        print(Fore.RED + f"❌ Шлях '{dir_path}' не існує." + Style.RESET_ALL)
        sys.exit(1)
    if not dir_path.is_dir():
        print(Fore.RED + f"❌ '{dir_path}' не є директорією." + Style.RESET_ALL)
        sys.exit(1)

    print(f"{Fore.CYAN}Структура директорії: {dir_path}{Style.RESET_ALL}")
    print_directory_tree(dir_path)

if __name__ == "__main__":
    main()