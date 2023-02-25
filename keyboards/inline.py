from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.loader import db


def generate_products_pagination(category_name, pagination=1):
    markup = InlineKeyboardMarkup()
    limit = 5
    count = db.get_count_product_by_category(category_name)
    max_pages = count // limit if count % limit == 0 else count // limit + 1
    offset = 0 if pagination == 1 else (pagination - 1) * limit
    # 2 -> 5   3 -> 10
    products = db.get_products_to_page(category_name, offset, limit)

    for product in products:  # [(1, 'Название', 123123123, '123123123', '123123', '123123'), ()]
        product_id, product_name = product[0], product[1]
        btn = InlineKeyboardButton(text=product_name, callback_data=f'product_{product_id}')  # product_1
        markup.add(btn)

    # 1 ->
    # <-  4  ->
    # <-  6
    if pagination == 1:
        page = InlineKeyboardButton(text=str(pagination), callback_data=f'page_{category_name}')
        next_page = InlineKeyboardButton(text='⏭', callback_data='next')
        markup.row(page, next_page)
    elif 1 < pagination < max_pages:
        prev_page = InlineKeyboardButton(text='⏮', callback_data='prev')
        page = InlineKeyboardButton(text=str(pagination), callback_data=f'page_{category_name}')
        next_page = InlineKeyboardButton(text='⏭', callback_data='next')
        markup.row(prev_page, page, next_page)
    elif pagination == max_pages:
        prev_page = InlineKeyboardButton(text='⏮', callback_data='prev')
        page = InlineKeyboardButton(text=str(pagination), callback_data=f'page_{category_name}')
        markup.row(prev_page, page)
    back_btn = InlineKeyboardButton(text='Назад', callback_data='back_categories')
    main_menu = InlineKeyboardButton(text='Главное меню', callback_data='main_menu')
    markup.row(back_btn, main_menu)

    return markup


def generate_product_detail(category_id, product_id, quantity=1):
    markup = InlineKeyboardMarkup()
    minus_btn = InlineKeyboardButton(text='➖', callback_data='minus')
    quant_btn = InlineKeyboardButton(text=str(quantity), callback_data='quantity')
    plus_btn = InlineKeyboardButton(text='➕', callback_data='plus')
    add_cart = InlineKeyboardButton(text='В корзину 💵', callback_data=f'cart_{product_id}')
    cart = InlineKeyboardButton(text='Корзина 🛒', callback_data='show_cart')
    back = InlineKeyboardButton(text='Назад', callback_data=f'back_category_{category_id}')
    main_menu = InlineKeyboardButton(text='Главное меню', callback_data='main_menu')
    markup.row(minus_btn, quant_btn, plus_btn)
    markup.row(add_cart, cart)
    markup.row(back, main_menu)
    return markup


def generate_cart_buttons(data):  # data['cart']
    markup = InlineKeyboardMarkup(row_width=1)
    for product_name, item in data.items():
        product_id = item['product_id']
        btn = InlineKeyboardButton(text=f'❌ {product_name} ❌', callback_data=f'remove_{product_id}')
        markup.add(btn)

    # Назад к категориям - back_categories
    # Очистить корзину - clear_cart
    # Подтвердить - submit_order
    # Главное меню - main_menu
    back_categories = InlineKeyboardButton(text='Назад к категориям', callback_data='back_categories')
    clear_cart = InlineKeyboardButton(text='Очистить корзину', callback_data='clear_cart')
    submit_order = InlineKeyboardButton(text='Подтвердить', callback_data='submit_order')
    main_menu = InlineKeyboardButton(text='Главное меню', callback_data='main_menu')
    markup.row(clear_cart, submit_order)
    markup.row(back_categories, main_menu)
    return markup
