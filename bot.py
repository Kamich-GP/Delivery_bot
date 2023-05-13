import telebot
from telebot import types

import bd, buttons
from geopy import Nominatim

# соединение с ботом
bot = telebot.TeleBot('6219564565:AAE2zKpaAEXWfSBF3DSD3cTzTE3GSJJHRWg')
geolocator = Nominatim(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64: x64)'
                                  'AppleWebKit/537.36 (KHTML, like Gecko)'
                                  'Chrome/108.0.0.0 Safari/537.36')


# обработка команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    # id пользователя
    global user_id
    user_id = message.from_user.id
    check_user = bd.checker(user_id)
    # Если пользователь есть в базе данных
    if check_user:
        bot.send_message(user_id, 'Привествую в нашем боте! Выберите пункт меню', reply_markup=buttons.product_name_buttons())
    # Если пользователя нет в базе данных
    else:
        bot.send_message(user_id, 'Приветствую в нашем боте! Прошу, введите имя!')
        # Перекидываем на этап получения имени
        bot.register_next_step_handler(message, get_name)


# Получение имени
def get_name(message):
    user_name = message.text
    bot.send_message(user_id, 'Отлично, теперь номер!', reply_markup=buttons.num_button())
    # Перекидываем на этап получения номера
    bot.register_next_step_handler(message, get_number, user_name)


# Получение номера
def get_number(message, user_name):
    # Если пользователь отправил номер по кнопке
    if message.contact:
        user_number = message.contact.phone_number
        # Запрашиваем локацию
        bot.send_message(user_id, 'Теперь отправьте локацию!', reply_markup=buttons.loc_button())
        # Перекидываем на этап получения локации
        bot.register_next_step_handler(message, get_location, user_name, user_number)
    # Если пользователь отправил номер в виде текста
    else:
        bot.send_message(user_id, 'Отправьте номер, используя кнопку!')
        # Обратно отправляем на этап получения номера
        bot.register_next_step_handler(message, get_number, user_name)


# Этап получении локации
def get_location(message, user_name, user_number):
    # Если отправил локацию по кнопке
    if message.location:
        user_location = geolocator.reverse(f"{message.location.longitude}, {message.location.latitude}")
        # Регистрируем пользователя
        bd.register(user_id, user_name, user_number, user_location)
        bot.send_message(user_id, 'Вы успешно зарегистрированы! Выберите пункт меню', reply_markup=buttons.product_name_buttons())
        bot.register_next_step_handler(message, text)
    # Если отправил локацию не по кнопке
    else:
        bot.send_message(user_id, 'Отправьте локацию через кнопку!')
        # Обратно отправляем на этап получения локации
        bot.register_next_step_handler(message, get_location, user_name, user_number)

#Сторона клиента
@bot.message_handler(content_types=['text'])
#Вывод информации о товаре
def text(message):
    all_products = [i[1] for i in bd.get_all_products()]
    if message.text in all_products:
        user_product = message.text
        full_info = bd.show_info(user_product)
        num_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in range(1,11):
            num_kb.add(str(i))
        bot.send_photo(user_id, photo=full_info[-1], caption=f'Описание: {full_info[0]}\n'
                                                             f'Цена: {full_info[1]}\n', reply_markup=num_kb)
        bot.register_next_step_handler(message, get_count, user_product, full_info)
    elif message.text == 'Корзина':
        full_cart = 'Ваша корзина:\n\n'
        for i in bd.show_cart(user_id):
            full_cart += f'Товар: {i[0]}\nКоличество: {i[1]}\nИтого: {i[2]}'
        bot.send_message(user_id, full_cart)
        bot.send_message(user_id, 'Выберите действие', reply_markup=buttons.cart_buttons())

def get_count(message, user_product, full_info):
    user_count = int(message.text)
    total_for_product = full_info[1] * user_count
    bd.add_to_cart(message.from_user.id, user_product, user_count, total_for_product)

    bot.send_message(user_id, 'Продукт(ы) добавлен(ы)', reply_markup=buttons.cart_button())
    bot.register_next_step_handler(message, text)
@bot.message_handler(commands=['admin'])
def admin_page(message):
    admin_id = 791555605

    # Проверяем если это админ то впускаем в админ панель
    if message.from_user.id == admin_id:
        bot.send_message(admin_id, 'Вы зашли в админ панель', reply_markup=buttons.admin_menu())


# Обработывает сообшении которые отправил юзер
@bot.message_handler(content_types=['text'])
def message(message):
    admin_id = 791555605

    # Проверяем если это админ то даем доступ к функциям
    if message.from_user.id == admin_id:
        if message.text == 'Добавить продукт':                                  # Убирает кнопки
            bot.send_message(admin_id, 'Введите название продукта', reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, get_product_name)
        elif message.text == 'Список продуктов':
            bot.send_message(admin_id, f'{bd.get_all_products()}')



def get_product_name(message):
    admin_id = 791555605
    pr_name = message.text

    bot.send_message(admin_id, 'Введите кол-во продукта')
    bot.register_next_step_handler(message, get_product_amount, pr_name)


def get_product_amount(message, pr_name):
    admin_id = 791555605
    pr_amount = int(message.text)

    bot.send_message(admin_id, 'Введите цену продукта')
    bot.register_next_step_handler(message, get_product_price, pr_name, pr_amount)


def get_product_price(message, pr_name, pr_amount):
    admin_id = 791555605
    pr_price = float(message.text)

    bot.send_message(admin_id, 'Введите описание товара')
    bot.register_next_step_handler(message, get_product_des, pr_name, pr_amount, pr_price)

def get_product_des(message, pr_name, pr_amount, pr_price):
    admin_id = 791555605
    pr_des = message.text

    bot.send_message(admin_id, 'Перейдите на сайт https://postimages.org/ и загрузите фото, затем скопируйте прямую ссылку и отправьте мне')
    bot.register_next_step_handler(message, get_product_photo, pr_name, pr_amount, pr_price, pr_des)

def get_product_photo(message, pr_name, pr_amount, pr_price, pr_des):
    admin_id = 791555605
    pr_photo = message.text
    bd.add_products(pr_name, pr_amount, pr_price, pr_des, pr_photo)

    bot.send_message(admin_id, 'Товар успешно добавлен!')
    bot.register_next_step_handler(message, message)
# Запуск бота
bot.polling()
