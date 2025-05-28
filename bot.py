import asyncio
import json
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

API_TOKEN = '8085251282:AAH3T4Zv48CahKqF7X2s3zLj9GwI4cWaDX8' 
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

NOTES_FILE = 'notes.json'

# Функції роботи з нотатками
def load_notes():
    if not os.path.exists(NOTES_FILE):
        return []
    try:
        with open(NOTES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_notes(notes):
    with open(NOTES_FILE, 'w', encoding='utf-8') as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)

# Стан машини
class NoteStates(StatesGroup):
    waiting_for_note = State()
    waiting_for_keyword = State()

# Команди
@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привіт! Я бот-помічник.\nДоступні команди:\n/add\n/list\n/search")

@dp.message(Command("add"))
async def cmd_add(message: Message, state: FSMContext):
    await message.answer("Введи текст нотатки:")
    await state.set_state(NoteStates.waiting_for_note)

@dp.message(NoteStates.waiting_for_note)
async def save_note(message: Message, state: FSMContext):
    notes = load_notes()
    notes.append(message.text)
    save_notes(notes)
    await message.answer("Нотатку збережено.")
    await state.clear()

@dp.message(Command("list"))
async def cmd_list(message: Message):
    notes = load_notes()
    if not notes:
        await message.answer("Немає нотаток.")
    else:
        await message.answer("\n".join(f"- {n}" for n in notes))

@dp.message(Command("search"))
async def cmd_search(message: Message, state: FSMContext):
    await message.answer("Введи ключове слово для пошуку:")
    await state.set_state(NoteStates.waiting_for_keyword)

@dp.message(NoteStates.waiting_for_keyword)
async def search_notes(message: Message, state: FSMContext):
    keyword = message.text.lower()
    notes = load_notes()
    found = [n for n in notes if keyword in n.lower()]
    if found:
        await message.answer("\n".join(f"- {n}" for n in found))
    else:
        await message.answer("Нічого не знайдено.")
    await state.clear()

# Запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
