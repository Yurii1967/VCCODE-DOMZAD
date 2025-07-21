

from collections import UserDict
from datetime import datetime, timedelta


# === Базові класи ===

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("❌ Телефон має містити рівно 10 цифр.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("❌ День народження має бути у форматі DD.MM.YYYY")
        super().__init__(value)


# === Record і AddressBook ===

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old, new):
        self.remove_phone(old)
        self.add_phone(new)

    def add_birthday(self, bday_str):
        self.birthday = Birthday(bday_str)

    def __str__(self):
        phones_str = ", ".join(str(p) for p in self.phones)
        bday = f", 🎂 Birthday: {self.birthday}" if self.birthday else ""
        return f"{self.name.value}: 📞 {phones_str}{bday}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        next_week = today + timedelta(days=7)
        upcoming = []

        for record in self.data.values():
            if record.birthday:
                bday = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
                bday_this_year = bday.replace(year=today.year)
                if today <= bday_this_year <= next_week:
                    upcoming.append(record)

        return upcoming


# === Декоратор для обробки помилок ===

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "⚠️ Недостатньо аргументів."
        except ValueError as e:
            return f"⚠️ {str(e)}"
        except Exception as e:
            return f"❌ Сталася помилка: {str(e)}"
    return wrapper


# === Обробники команд ===

@input_error
def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name)
    message = "📞 Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "✅ Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_phone(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "✅ Телефон оновлено."
    return "❌ Контакт не знайдено."


@input_error
def show_phones(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        return f"{name}: {', '.join(str(p) for p in record.phones)}"
    return "❌ Контакт не знайдено."


@input_error
def show_all(args, book):
    if not book.data:
        return "📭 Адресна книга порожня."
    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book):
    name = args[0]
    birthday_str = args[1]
    record = book.find(name)
    if record:
        record.add_birthday(birthday_str)
        return f"🎉 День народження додано для {name}."
    return "❌ Контакт не знайдено."


@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        if record.birthday:
            return f"🎂 День народження {name}: {record.birthday.value}"
        return "ℹ️ День народження не вказано."
    return "❌ Контакт не знайдено."


@input_error
def birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "🎉 Немає днів народження протягом тижня."
    lines = [f"{rec.name.value}: {rec.birthday.value}" for rec in upcoming]
    return "🎁 Дні народження на тиждень:\n" + "\n".join(lines)


# === Допоміжна функція ===

def parse_input(user_input):
    parts = user_input.strip().split()
    if not parts:
        return "", []
    return parts[0].lower(), parts[1:]


# === Основна функція ===

def main():
    book = AddressBook()
    print("🤖 Вітаю у боті-асистенті!")
    while True:
        user_input = input(">>> ")
        command, args = parse_input(user_input)

        if command in ("close", "exit"):
            print("👋 До побачення!")
            break
        elif command == "hello":
            print("Привіт! Чим можу допомогти?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_phone(args, book))
        elif command == "phone":
            print(show_phones(args, book))
        elif command == "all":
            print(show_all(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("❌ Невідома команда. Спробуйте ще раз.")


if __name__ == "__main__":
    main()
