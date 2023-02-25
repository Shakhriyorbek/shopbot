from telebot.types import LabeledPrice, ShippingOption
from .shipping_product import Product


def generate_product_invoice(product_data): # data['cart']
    query = Product(
        title='Лучший телеграм бот магазин',
        description=  '\n'.join([product_name for product_name in product_data]),
        start_parameter='create_invoice_products',
        currency='UZS',
        prices=[LabeledPrice(
            label=f"{product_data[product_name]['quantity']} - {product_name}",
            amount= int(product_data[product_name]['quantity']) * int(product_data[product_name]['price']) * 100
        ) for product_name in product_data],
        provider_token='YOUR TOKEN HERE',
        need_name=True
    )
    return query


EXPRESS_SHIPPING = ShippingOption(
    id='post_express',
    title='До 3х часов'
).add_price(LabeledPrice('До 3х часов', 25_000_00))
