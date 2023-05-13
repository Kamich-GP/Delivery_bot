from telebot import types

import bd


# Создание кнопки отправки номера
def num_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Непосредственно сама кнопка
    number_button = types.KeyboardButton('Отправить номер', request_contact=True)
    # Добавить пространство под кнопку
    kb.add(number_button)
    # Возвращаем результат
    return kb


# Создание кнопки отправки локации
def loc_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Непосредственно сама кнопка
    location_button = types.KeyboardButton('Отправить локацию', request_location=True)
    # Добавить пространство под кнопку
    kb.add(location_button)
    # Возвращаем результат
    return kb

def cart_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for i in bd.get_all_products():
        kb.add(i[1])
    button = types.KeyboardButton('Корзина')
    kb.add(button)
    return kb


def product_name_buttons():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in bd.get_names():
        kb.add(i[0])

    return kb

def cart_buttons():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    order = types.KeyboardButton('Заказать')
    delete = types.KeyboardButton('Удалить товары')

    kb.add(order, delete)
    return kb


# Главные кнопки админ панели
def admin_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    button1 = types.KeyboardButton('Добавить продукт')
    button2 = types.KeyboardButton('Редактирововать продукт')
    button3 = types.KeyboardButton('Удалить продукт')
    button4 = types.KeyboardButton('Список продуктов')

    kb.add(button1, button2, button3, button4)

    return kb


# Под категории редактирования продукта
def admin_update_categories():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    button1 = types.KeyboardButton('Изменить название продукта')
    button2 = types.KeyboardButton('Изменить кол-во продукта')
    button3 = types.KeyboardButton('Изменить цену продукта')
    button4 = types.KeyboardButton('Изменить описание продукта')
    button5 = types.KeyboardButton('Изменить фото продукта')

    kb.add(button1, button2, button3, button4, button5)

    return kb
