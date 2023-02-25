from data.loader import db
from parsing.parser import Parser
from pprint import pprint

# db.create_categories_table()
# db.create_products_table()
# db.create_users_table()

# parser = Parser()
# all_data = parser.get_data()
# pprint(all_data)
#
#
#
# for category_name in all_data:
#     db.insert_category(category_name)
#     category_id = db.category_id_by_name(category_name)
#     print(category_name, category_id)
#
#     for product in all_data[category_name]:
#         product_title = product['product_title']
#         product_price = product['product_price']
#         product_description = product['product_description']
#         product_image_link = product['product_image_link']
#         product_link = product['product_link']
#         db.insert_into_products(product_name=product_title,
#                                 product_description=product_description,
#                                 product_link=product_link,
#                                 product_price=product_price,
#                                 product_image_link=product_image_link,
#                                 category_id=category_id)


