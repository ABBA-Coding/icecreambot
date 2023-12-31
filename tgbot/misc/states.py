from aiogram.dispatcher.filters.state import StatesGroup, State


class UserRegisterState(StatesGroup):
    get_lang = State()
    get_name = State()
    get_contact = State()
    get_location = State()


class MainMenuState(StatesGroup):
    get_menu = State()


class SettingsState(StatesGroup):
    get_buttons = State()
    change_lang = State()
    get_lang = State()
    change_address = State()


class BuyState(StatesGroup):
    get_location = State()
    get_category = State()
    get_product = State()
    get_cart = State()
    get_phone = State()
    get_payment_method = State()
    get_approve = State()
    get_billing = State()


class ReviewState(StatesGroup):
    get_review = State()
