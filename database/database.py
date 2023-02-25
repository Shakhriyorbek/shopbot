import sqlite3


class DataBase:
    def __init__(self):
        self.database = sqlite3.connect('shop.db', check_same_thread=False)

    def manager(self, sql, *args,
                commit: bool = False,
                fetchone: bool = False,
                fetchall: bool = False):
        with self.database as db:
            cursor = db.cursor()
            cursor.execute(sql, args)
            if commit:
                result = db.commit()
            if fetchone:
                result = cursor.fetchone()
            if fetchall:
                result = cursor.fetchall()
            return result

    def create_categories_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS categories(
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name VARCHAR(50) UNIQUE
        )'''
        self.manager(sql, commit=True)

    def create_products_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS products(
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name VARCHAR(255) UNIQUE,
            product_price INTEGER,
            product_link TEXT,
            product_image_link TEXT,
            product_description TEXT,
            category_id INTEGER REFERENCES categories(category_id)
        )
        '''
        self.manager(sql, commit=True)

    def insert_category(self, category_name):
        sql = '''INSERT OR IGNORE INTO categories(category_name) VALUES (?)'''
        self.manager(sql, category_name, commit=True)

    def category_id_by_name(self, category_name):
        sql = '''SELECT category_id FROM categories WHERE category_name = ?'''
        return self.manager(sql, category_name, fetchone=True)[0]

    def insert_into_products(self, product_name, product_price, product_link,
                             product_image_link, product_description, category_id):
        sql = '''INSERT OR IGNORE INTO products(product_name, product_price, product_link,product_image_link, product_description, category_id)
        VALUES (?,?,?,?,?,?)
        '''
        self.manager(sql, product_name, product_price, product_link,
                     product_image_link, product_description, category_id, commit=True)

    def create_users_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS users(
            telegram_id BIGINT PRIMARY KEY,
            full_name VARCHAR(100),
            contact VARCHAR(20) UNIQUE
        )
        '''
        self.manager(sql, commit=True)

    def get_user_by_id(self, telegram_id):
        sql = '''
        SELECT * FROM users WHERE telegram_id = ?
        '''
        return self.manager(sql, telegram_id, fetchone=True)

    def register_user(self, telegram_id, full_name, contact):
        sql = '''
        INSERT INTO users(telegram_id, full_name, contact) VALUES (?,?,?)
        '''
        self.manager(sql, telegram_id, full_name, contact, commit=True)

    def get_categories(self):
        sql = '''
        SELECT category_name FROM categories
        '''
        return self.manager(sql, fetchall=True)

    def get_count_product_by_category(self, category_name):
        sql = '''
        SELECT COUNT(product_id) FROM products
        WHERE category_id = (
            SELECT category_id FROM categories WHERE category_name = ?
        )
        '''
        return self.manager(sql, category_name, fetchone=True)[0]  # (14, ) -> 14

    def get_products_to_page(self, category_name, offset, limit):
        sql = '''
        SELECT * FROM products
        WHERE category_id = (
            SELECT category_id FROM categories WHERE category_name = ?
        )
        LIMIT ?
        OFFSET ?
        '''
        return self.manager(sql, category_name, limit, offset, fetchall=True)

    def get_product_detail(self, product_id):
        sql = '''
        SELECT * FROM products WHERE product_id = ?
        '''
        return self.manager(sql, product_id, fetchone=True)
        # (1, 'Название товара', 123123, ''')
        # [(1, 'Название товара', 123123, ''')]

    def get_category_name_by_id(self, category_id):
        sql = '''
        SELECT category_name FROM categories WHERE category_id = ?
        '''
        return self.manager(sql, category_id, fetchone=True)[0]
