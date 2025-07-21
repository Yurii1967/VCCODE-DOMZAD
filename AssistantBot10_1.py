

from collections import UserDict
from datetime import datetime, timedelta, date


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
        if not value.isdigit() or len(value) < 5:
            raise ValueError("❌ Невірний номер телефону. Має містити щонайменше 5 цифр.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            birthday = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(birthday)
        except ValueError:
            raise ValueError("❌ Невірний формат дати. Використовуйте DD.MM.YYYY")


# === Клас Record ===

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        self.phones.append(phone)

    def add_birthday(self, birthday_str):
        self.birthday = Birthday(birthday_str)

    def __str__(self):
        phones_str = ', '.join(str(phone) for phone in self.phones)
        birthday_str = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "немає"
        return f"👤 {self.name.value}: 📞 {phones_str}; 🎂 {birthday_str}"


# === Клас AddressBook ===

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def get_upcoming_birthdays(self):
        today = date.today()
        upcoming = []

        for record in self.data.values():
            if record.birthday:
                birthday = record.birthday.value
                next_birthday = birthday.replace(year=today.year)

                if next_birthday < today:
                    next_birthday = birthday.replace(year=today.year + 1)

                delta = (next_birthday - today).days

                if 0 <= delta <= 7:
                    upcoming.append({
                        "name": record.name.value,
                        "birthday": next_birthday.strftime("%d.%m.%Y")
                    })

        return upcoming


# === Функції бота ===

def parse_input(user_input):
    cmd, *args = user_input.strip().split()
    return cmd.lower(), args


def main():
    book = AddressBook()

    print("📘 Адресна книга. Введіть команду (add, add-birthday, show-birthday, birthdays, exit):")

    while True:
        user_input = input(">>> ")
        command, args = parse_input(user_input)

        if command == "add":
            try:
                name, phone = args
                record = Record(name)
                record.add_phone(phone)
                book.add_record(record)
                print("✅ Контакт додано.")
            except Exception as e:
                print(f"❌ {e}")

        elif command == "add-birthday":
            try:
                name, birthday = args
                record = book.data.get(name)
                if record:
                    record.add_birthday(birthday)
                    print("✅ День народження додано.")
                else:
                    print("❌ Контакт не знайдено.")
            except Exception as e:
                print(f"❌ {e}")

        elif command == "show-birthday":
            name = args[0]
            record = book.data.get(name)
            if record and record.birthday:
                print(f"🎂 День народження {name}: {record.birthday.value.strftime('%d.%m.%Y')}")
            else:
                print("❌ День народження не знайдено.")

        elif command == "birthdays":
            upcoming = book.get_upcoming_birthdays()
            if upcoming:
                print("🎉 Привітання цього тижня:")
                for entry in upcoming:
                    print(f" - {entry['name']} ({entry['birthday']})")
            else:
                print("📭 Немає днів народження на цьому тижні.")

        elif command == "exit":
            print("👋 До побачення!")
            break

        else:
            print("❌ Невідома команда.")


# === Запуск ===

if __name__ == "__main__":
    main()
