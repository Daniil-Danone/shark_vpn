from aiogram.fsm.state import StatesGroup, State


class BalanceState(StatesGroup):
    default = State()
    cash_in = State()
    cash_out = State()
    wallet = State()