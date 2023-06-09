import sqlite3

# Подключение к базе данных
connection = sqlite3.connect('delivery.db', check_same_thread=False)
# Связь между Python и SQL
sql = connection.cursor()

# Создание таблицы пользователей
sql.execute('CREATE TABLE IF NOT EXISTS users'
            '(user_id INTEGER, '
            'name TEXT,'
            'number TEXT,'
            'location TEXT);')
# Создание таблицы товаров
sql.execute('CREATE TABLE IF NOT EXISTS products'
            '(pr_id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'pr_name TEXT,'
            'pr_amount INTEGER,'
            'pr_price REAL,'
            'pr_des TEXT,'
            'pr_photo TEXT);')
# Создание таблицы корзины пользователя
sql.execute('CREATE TABLE IF NOT EXISTS user_cart'
            '(user_id INTEGER,'
            'user_product TEXT,'
            'product_quantity INTEGER,'
            'total REAL);')
# Создание таблицы заказов
sql.execute('CREATE TABLE IF NOT EXISTS orders'
            '(id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'user_id INTEGER,'
            'user_location TEXT,'
            'payment TEXT,'
            'total_charge REAL);')


##Методы для пользователя##
# Регистрация
def register(id, name, number, location):
    sql.execute('INSERT INTO users VALUES (?, ?, ?, ?);', (id, name, number, location))
    # Фиксируем изменения
    connection.commit()


def checker(id):
    check = sql.execute('SELECT user_id FROM users WHERE user_id=?;', (id,))

    if check.fetchone():
        return True
    else:
        return False

#Вся информация о товаре
def show_info(pr_name):
    sql.execute('SELECT pr_des, pr_price, pr_photo FROM products WHERE pr_name = ?;', (pr_name,))
    product = sql.fetchone()

    return product
# Добавление продуктов
def add_products(pr_name, pr_amount, pr_price, pr_desc, pr_photo):
    sql.execute('INSERT INTO products (pr_name, pr_amount, pr_price, pr_des, pr_photo) '
                'VALUES (?, ?, ?, ?, ?);',
                (pr_name, pr_amount, pr_price, pr_desc, pr_photo))

    connection.commit()


# Удаление продуктов
def delete_exact_product(pr_name):
    sql.execute('DELETE FROM products WHERE pr_name=?;', (pr_name,))

    connection.commit()


# Обновление конкретной информации продукта
def update_exact_product_info(action, new_data, pr_name):
    if action == 'Изменить название продукта':
        sql.execute('UPDATE products SET pr_name=?, WHERE pr_name=?;', (new_data, pr_name))

    elif action == 'Изменить цену продукта':
        sql.execute('UPDATE products SET pr_price=?, WHERE pr_name=?;', (new_data, pr_name))

    elif action == 'Изменить кол-во продукта':
        sql.execute('UPDATE products SET pr_amount=?, WHERE pr_name=?;', (new_data, pr_name))

    elif action == 'Изменить описание продукта':
        sql.execute('UPDATE products SET pr_des=?, WHERE pr_name=?;', (new_data, pr_name))

    elif action == 'Изменить фото продукта':
        sql.execute('UPDATE products SET pr_photo=?, WHERE pr_name=?;', (new_data, pr_name))

    connection.commit()


def get_all_products():
    all_products = sql.execute('SELECT * FROM products;')

    return all_products.fetchall()

def get_names():
    names = sql.execute('SELECT pr_name FROM products;').fetchall()
    return names


##Методы для корзины##
#Добавление товаров в корзину
def add_to_cart(user_id, user_product, product_quantity, total):
    sql.execute('INSERT INTO user_cart VALUES(?,?,?,?);',
                (user_id, user_product, product_quantity, total))
    connection.commit()

#Удаление товаров из корзины
def del_from_cart(user_id):
    sql.execute('DELETE FROM user_cart WHERE user_id = ?;', (user_id))
    connection.commit()

#Отображение товаров из корзины
def show_cart(user_id):
    sql.execute('SELECT user_product, product_quantity, total FROM user_cart WHERE user_id = ?', (user_id,))
    cart = sql.fetchall()
    return cart