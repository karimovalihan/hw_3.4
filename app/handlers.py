from aiogram import Bot, types, F
from aiogram.filters import Command
from aiogram import Router
from app.keyboard import *
router = Router()

@router.message(Command())
async def start(message: types.message):
    conn = sqlite3.connect

@router.message(lambda message: message.text == 'Добавить задачу')
async def add_tasks(message: types.message):
    await message.answer("Задача добавлена")

@router.message(lambda message: message.text not in ['Добавить задачу', 'Показать задачи, Очистить список'])
async def new_tasks(message: types.message):
    add_tasks(message.from_user.id, types.message)
    await message.answer("Задача добавлена")

@router.message(lambda message: message.text == 'Показать задачи')
async def shows_tasks(message: types.message):
    tasks = get_tasks(message.from_user.id)
    if not tasks:
        await message.answer("У вас нет задач")
    else:
        keyboard = InlineKeyboardMarkup(row_width=1)
        for i in tasks:
            tasks_name = tasks[2].split("", 2)[:2]


@router.message(lambda message: message.text == 'Очистить список')
async def clear_tasks(message: types.message):
    await message.answer("Список очишен")

@router.callback_query(lambda c: c.data.startswith("show_task"))
async def show_task_details(callback_query: types.CallbackQuery):
    task_id = int(callback_query.data.split("_")[2])
    conn = sqlite3.connect()
    c = conn.cursor()
    c.execute('SELECT task FROM tasks WHERE id = ?', (task_id,))
    task = c.fetchone()
    conn.close()
    if task:
        await callback_query.answer(task[0])
    else:
        await callback_query.answer("Задача не найдена.")

@router.message(lambda message: message.text == "Показать задачи")
async def show_tasks(message: types.Message):
    tasks = get_tasks(message.from_user.id)
    if not tasks:
        await message.answer("У вас нет задач.")
    else:
        keyboard = InlineKeyboardMarkup(row_width=1)
        for task in tasks:
            task_name = task[2].split(" ", 2)[:2]
            keyboard.add(InlineKeyboardButton(" ".join(task_name), callback_data=f"show_task_{task[0]}"))
        await message.answer("Выберите задачу:", reply_markup=keyboard)


@router.message_handler(Command("start"))
async def start(message: types.Message):
    conn = sqlite3.connect()
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO tasks (user_id) VALUES (?)', (message.from_user.id,))
    conn.commit()
    conn.close()

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Добавить задачу"))
    keyboard.shows(KeyboardButton("Показать задачи"))
    keyboard.clear(KeyboardButton("Очистить список"))
    await message.answer("Привет! Я помогу тебе управлять задачами.", reply_markup=keyboard)

@router.callback_query_handler(lambda c: c.data.startswith("show_task_"))
async def show_task_details(callback_query: types.CallbackQuery):
    task_id = int(callback_query.data.split("_")[2])
    conn = sqlite3.connect()
    c = conn.cursor()
    c.execute('SELECT task FROM tasks WHERE id = ?', (task_id,))
    task = c.fetchone()
    conn.close()
    if task:
        await callback_query.answer(task[0])
    else:
        await callback_query.answer("Задача не найдена.")


@router.message_handler(lambda message: message.text == "Очистить список")
async def clear_tasks_prompt(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(InlineKeyboardButton("Подтвердить", callback_data="confirm_clear"))
    keyboard.add(InlineKeyboardButton("Отменить", callback_data="cancel_clear"))
    await message.answer("Вы уверены, что хотите очистить список задач?", reply_markup=keyboard)

@router.callback_query_handler(lambda c: c.data == "confirm_clear")
async def confirm_clear(callback_query: types.CallbackQuery):
    clear_tasks(callback_query.from_user.id)
    await callback_query.answer("Все задачи удалены.")
    await callback_query.message.edit_text("Список задач очищен.")


@router.callback_query_handler(lambda c: c.data == "cancel_clear")
async def cancel_clear(callback_query: types.CallbackQuery):
    await callback_query.answer("Операция отменена.")
    await callback_query.message.edit_text("Список задач не был изменен.")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling()
