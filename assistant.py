import json
import os

class Assistant:
    def __init__(self, filename='notes.json'):
        self.filename = filename
        self.notes = self.load_notes()

    def load_notes(self):
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_notes(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.notes, file, ensure_ascii=False, indent=2)

    def add_note(self, note):
        self.notes.append(note)
        self.save_notes()

    def list_notes(self):
        return self.notes

    def search_notes(self, keyword):
        return [note for note in self.notes if keyword.lower() in note.lower()]


def main():
    assistant = Assistant()

    while True:
        command = input("Введіть команду (/add, /list, /search, /exit): ").strip()

        if command == "/add":
            note = input("Введіть нотатку: ")
            assistant.add_note(note)
            print("Нотатку додано.")
        elif command == "/list":
            notes = assistant.list_notes()
            print("Нотатки:")
            for note in notes:
                print(f"- {note}")
        elif command == "/search":
            keyword = input("Ключове слово: ")
            results = assistant.search_notes(keyword)
            print("Результати пошуку:")
            for note in results:
                print(f"- {note}")
        elif command == "/exit":
            print("До побачення!")
            break
        else:
            print("Невідома команда.")

if __name__ == "__main__":
    main()
