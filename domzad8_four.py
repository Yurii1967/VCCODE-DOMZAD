


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter user name."
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter the argument for the command."
    return inner

contacts = {}

@input_error
def add_contact(args):
    name, phone = args
    contacts[name] = phone
    return "Contact added."

@input_error
def change_contact(args):
    name, phone = args
    if name not in contacts:
        raise KeyError
    contacts[name] = phone
    return "Contact updated."

@input_error
def get_phone(args):
    name = args[0]
    return f"{name}: {contacts[name]}"

@input_error
def show_all(args=None):
    if not contacts:
        return "No contacts found."
    return '\n'.join([f"{name}: {phone}" for name, phone in contacts.items()])

def parse_command(user_input):
    parts = user_input.strip().split()
    command = parts[0].lower()
    args = parts[1:]
    return command, args

def main():
    print("Hello! I'm your assistant bot.")
    while True:
        user_input = input("Enter a command: ")
        if user_input.lower() in ["exit", "close", "good bye"]:
            print("Good bye!")
            break

        command, args = parse_command(user_input)

        if command == "add":
            print(add_contact(args))
        elif command == "change":
            print(change_contact(args))
        elif command == "phone":
            print(get_phone(args))
        elif command == "all":
            print(show_all())
        else:
            print("Unknown command. Please try again.")

if __name__ == "__main__":
    main()
