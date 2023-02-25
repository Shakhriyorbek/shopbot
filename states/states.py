from telebot.handler_backends import State, StatesGroup

class CartState(StatesGroup):
    cart = State()


# class Questions(StatesGroup):
#     name = State()
#     last_name = State()
#     age = State()
#     work = State()
#