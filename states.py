from aiogram.fsm.state import StatesGroup, State


class LifePathStates(StatesGroup):
    WAITING_FOR_BIRTHDATE = State()


class CompatibilityStates(StatesGroup):
    WAITING_FOR_DATES = State()

class NumerologyStates(StatesGroup):
    WAITING_FOR_QUESTION = State()

__all__ = ()
