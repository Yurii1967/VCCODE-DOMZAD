

        
from pathlib import Path

to_cats_list_path = Path("Probe/My_probe/cats.txt").absolute()

def get_cats_info(file_path):
    cats = []
    try:
        with open(file_path, "r", encoding="UTF-8") as f:
            for line in f:
                value_list = line.strip().split(',')
                key_list = ["id", "Nickname", "Age in years"]
                cat = dict(zip(key_list, value_list))
                cats.append(cat)
        return cats
    except FileNotFoundError:
        print(f"No file {file_path}")

# Передаємо саму змінну, а не рядок
id_cat = get_cats_info(to_cats_list_path)
print(id_cat)
