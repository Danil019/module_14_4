from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import crud_functions as cf
import asyncio

key_api = '7663863093:AAHBqmiFkF15GWjTPKjsmgb68wyN-Iz8QVg'
bot = Bot(token=key_api)
dp = Dispatcher(bot, storage = MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard = True)
button_main = KeyboardButton(text = 'Рассчитать')
button_info = KeyboardButton(text = 'Информация')
button_buy = KeyboardButton(text = 'Купить')
kb.add(button_main, button_info, button_buy)

kb2 = InlineKeyboardMarkup(resize_keyboard = True)
button_age = InlineKeyboardButton(text = 'Рассчитать', callback_data='calories')
button_form = InlineKeyboardButton(text = 'Формула', callback_data='formulas')
kb2.add(button_age, button_form)

kb3 = InlineKeyboardMarkup(resize_keyboard = True)
button_pr = InlineKeyboardButton(text = 'Продукт1', callback_data="product_buying")
button_pr2 = InlineKeyboardButton(text = 'Продукт2', callback_data="product_buying")
button_pr3 = InlineKeyboardButton(text = 'Продукт3', callback_data="product_buying")
button_pr4 = InlineKeyboardButton(text = 'Продукт4', callback_data="product_buying")
kb3.add(button_pr, button_pr2, button_pr3, button_pr4)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=["start"])
async def start(message):
    cf.get_all_products()
    await message.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup = kb)

@dp.message_handler(text = "Рассчитать")
async def main_menu(message):
    await message.answer("Выберите опцию:", reply_markup = kb2)

@dp.callback_query_handler(text = "calories")
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(first = message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(second = message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    await state.update_data(third = message.text)
    data = await state.get_data()
    bmr = 10 * float(data['third']) + 6.25 * float(data['second']) - 5 * float(data['first']) + 5
    await message.answer(f"Ваша норма калорий: {bmr}")
    await state.finish()

@dp.callback_query_handler(text = "formulas")
async def get_formulas(call):
    await call.message.answer('10 x вес(кг) + 6.25 x рост(см) - 5 * возраст + 5')
    await call.answer()

@dp.message_handler(text="Купить")
async def get_buying_list(message):
    for i in range(1, 5):
        with open(f"{i}.jpg", "rb") as img:
            await message.answer(f"Название: Продукт {cf.get_all_products()[i-1][0]} | Описание: описание {cf.get_all_products()[i-1][1]} | Цена: {cf.get_all_products()[i-1][2]}")
            await message.answer_photo(img)
    cf.connection.close()
    await message.answer("Выберите продукт для покупки:", reply_markup = kb3)

@dp.callback_query_handler(text = "product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")

@dp.message_handler()
async def all_messages(message):
    await message.answer("Введите команду /start, чтобы начать общение.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)