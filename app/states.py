from aiogram.fsm.state import State, StatesGroup

class Work(StatesGroup):
    process = State()

class Login(StatesGroup):
    number = State()
