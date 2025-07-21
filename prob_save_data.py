

import pickle
from collections import UserDict


# === Класи для адресної книги ===

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) < 5:
            raise ValueError("Телефон має містити щонайменше 5 цифр.")
        super().__init__(value)


class Record:
    def __init__(self, name: Name):
        self.name = name
        self.phones = []

    def add_phone(self, phone: Phone):
        self.phones.append(phone)

    def __str__(self):
        phones_str = ", ".join(str(p) for p in self.phones)
        return f"{self.name}: {phones_str}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]


# === Серіалізація/Десеріалізація ===

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


# === Основний цикл програми ===

def main():
    book = load_data()

    while True:
        command = input("Введіть команду (add, show, exit): ").strip().lower()

        if command == "add":
            name = input("Ім'я: ")
            phone = input("Телефон: ")
            try:
                record = book.find(name)
                if not record:
                    record = Record(Name(name))
                    book.add_record(record)
                record.add_phone(Phone(phone))
                print("✅ Контакт додано.")
            except ValueError as e:
                print(f"❌ Помилка: {e}")

        elif command == "show":
            for record in book.values():
                print(record)

        elif command == "exit":
            save_data(book)
            print("💾 Адресна книга збережена. До зустрічі!")
            break

        else:
            print("❓ Невідома команда. Доступні: add, show, exit")


if __name__ == "__main__":
    main()
