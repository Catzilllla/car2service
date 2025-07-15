from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.filters import Command
from app.models.schemas import AppointmentForm
from app.configs import config

router = Router()

class Form(StatesGroup):
    name = State()
    phone = State()
    car_model = State()
    problem = State()
    appointment_time = State()

@router.message(Command(commands=['start', 'record']))
async def start_dialog(message: Message, state: FSMContext):
    await message.answer("Привет! Как вас зовут?")
    await state.set_state(Form.name)

@router.message(Form.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Ваш номер телефона?")
    await state.set_state(Form.phone)

@router.message(Form.phone)
async def get_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Марка автомобиля?")
    await state.set_state(Form.car_model)

@router.message(Form.car_model)
async def get_car(message: Message, state: FSMContext):
    await state.update_data(car_model=message.text)
    await message.answer("Какая проблема с автомобилем?")
    await state.set_state(Form.problem)

@router.message(Form.problem)
async def get_problem(message: Message, state: FSMContext):
    await state.update_data(problem=message.text)
    await message.answer("Желаемое время записи?")
    await state.set_state(Form.appointment_time)

@router.message(Form.appointment_time)
async def get_time(message: Message, state: FSMContext, bot):
    data = await state.update_data(appointment_time=message.text)
    form = AppointmentForm(**data)
    await message.answer("Спасибо! Мы записали вашу заявку.")
    await bot.send_message(config.TG_CHANNEL_ID, form.format_for_channel())
    await state.clear()