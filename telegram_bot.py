import logging
import os
from functools import partial

import redis
from dotenv import load_dotenv
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)

from api_handler import (add_product_to_card, get_all_products, get_card,
                         get_card_items, get_image, get_product,
                         remove_cart_item)
from logging_handler import TelegramLogsHandler
from storing_data import FishShopPersistence

logger = logging.getLogger(__name__)

START, HANDLE_MENU, HANDLE_DESCRIPTION, HANDLE_CART = range(4)


def start(products, update: Update, context: CallbackContext) -> None:
    keyboard = []
    for product in products.get('data'):
        product_name = product.get('name')
        product_id = product.get('id')
        key = [InlineKeyboardButton(product_name, callback_data=product_id)]
        keyboard.append(key)
    card_keyboard = [InlineKeyboardButton('Корзина', callback_data='all_card')]
    keyboard.append(card_keyboard)
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        'Hello! Please choose:',
        reply_markup=reply_markup
        )
    return HANDLE_DESCRIPTION


def handle_describtion(elastickpath_access_token, update: Update, context: CallbackContext) -> None:
    message_id = update.effective_message.message_id
    chat_id = update.effective_message.chat_id
    query = update.callback_query
    query.answer()
    logger.info('user was there')
    logger.info(query.data)
    if '|' in query.data:
        logger.info('user is here')
        product_id, card = query.data.strip('|')
        _, quantity = card.split(':')
        add_product_to_card(chat_id, product_id, elastickpath_access_token, quantity)
        logger.info(f'Succed added product to card')
        return HANDLE_MENU
    context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    product_id = query.data
    product_payload = get_product(product_id, elastickpath_access_token)
    product_name = product_payload.get('data').get('name')
    product_price = product_payload.get('data').get('meta').get('display_price').get('with_tax').get('formatted')
    product_text = product_payload.get('data').get('description')
    product_image_id = product_payload.get('data').get('relationships').get('main_image').get('data').get('id')
    path = get_image(product_image_id, elastickpath_access_token)
    product_describtion = f'{product_name}\n{product_price}\n\n{product_text}'
    keyboard = [
        [
            InlineKeyboardButton('1 kg', callback_data=f'{product_id}|card:1'),
            InlineKeyboardButton('2 kg', callback_data=f'{product_id}|card:2'),
            InlineKeyboardButton('3 kg', callback_data=f'{product_id}|card:3')
            ],
        [InlineKeyboardButton('Корзина', callback_data='productcard')],
        [InlineKeyboardButton('Назад', callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    with open(path, 'rb') as file:
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=file,
            caption=product_describtion,
            reply_markup=reply_markup
            )
    return HANDLE_MENU


def handle_menu(products, update: Update, context: CallbackContext) -> None:
    message_id = update.effective_message.message_id
    chat_id = update.effective_message.chat_id
    context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    keyboard = []
    for product in products.get('data'):
        product_name = product.get('name')
        product_id = product.get('id')
        key = [InlineKeyboardButton(product_name, callback_data=product_id)]
        keyboard.append(key)
    card_keyboard = [InlineKeyboardButton('Корзина', callback_data='all_card')]
    keyboard.append(card_keyboard)
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(
        chat_id=chat_id,
        text='Please choose:',
        reply_markup=reply_markup
        )
    return HANDLE_DESCRIPTION


def handle_cart(elastickpath_access_token, update: Update, context: CallbackContext):
    chat_id = update.effective_message.chat_id
    cards = get_card(chat_id, elastickpath_access_token)
    logger.info(f'Handle card respon api\n{cards}')
    card_items = get_card_items(chat_id, elastickpath_access_token)
    logger.info(f'Handle card respon api\n{card_items}')
    card_total_price = card_items.get('data').get('meta').get('display_price').get('with_tax').get('formatted')
    products_list = []
    for item in card_items.get('data'):
        logger.info(f'Handle card respon api\n{item}')
        item_name = item.get('name')
        item_quantity = item.get('quantity')
        item_price_per_item = item.get('meta').get('display_price').get('with_tax').get('unit').get('formatted')
        item_total_price = item.get('meta').get('display_price').get('with_tax').get('value').get('formatted')
        products_describtion = f'{item_name}\n{item_price_per_item} per kg\n{item_quantity}kg in cart for {item_total_price}\n\n'
        products_list.append(products_describtion)
    all_products = ''.join(product for product in products_list)
    card_message = f'{all_products}Total:{card_total_price}'
    context.bot.send_message(
        chat_id=chat_id,
        text=card_message,
    )
    return HANDLE_CART


def handle_error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning(
        f'Update {update} caused error {context.error},\
        traceback {context.error.__traceback__}'
        )


def end_conversation(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Пока!'
        )
    return ConversationHandler.END


def main():
    load_dotenv()
    token = os.getenv('TOKEN_TELEGRAM')
    user_id = os.getenv('TG_USER_ID')
    redis_host = os.getenv('REDDIS_HOST')
    redis_port = os.getenv('REDDIS_PORT')
    redis_pass = os.getenv('REDDIS_PASS')
    elastickpath_access_token = os.getenv('ELASTICPATH_ACCESS_TOKEN')
    redis_base = redis.Redis(
        host=redis_host,
        port=redis_port,
        password=redis_pass
        )
    products = get_all_products(elastickpath_access_token)
    persistence = FishShopPersistence(redis_base)
    logging_token = os.getenv('TG_TOKEN_LOGGING')
    logging_bot = Bot(token=logging_token)
    logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
    logger.setLevel(logging.DEBUG)
    logger.addHandler(TelegramLogsHandler(tg_bot=logging_bot, chat_id=user_id))
    logger.info('Fish store bot запущен')
    """Start the bot."""
    updater = Updater(token, persistence=persistence)
    dispatcher = updater.dispatcher
    partial_start = partial(start, products)
    partial_handle_menu = partial(handle_menu, products)
    partial_handle_describtion = partial(handle_describtion, elastickpath_access_token)
    partial_handle_cart = partial(handle_cart, elastickpath_access_token)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", partial_start)],
        states={
            START: [
                MessageHandler(Filters.text, partial_start),
                ],
            HANDLE_DESCRIPTION: [
                CallbackQueryHandler(partial_handle_describtion),
                CallbackQueryHandler(partial_handle_describtion, pattern="^(\S{3,}card[1-3])$"),
                ],
            HANDLE_MENU: [
                CallbackQueryHandler(partial_handle_menu, pattern="^(back)$"),
                CallbackQueryHandler(partial_handle_describtion, pattern="^(\S{3,}card[1-3])$"),
                CallbackQueryHandler(partial_handle_cart, pattern="^(productcard)$")
            ],
            HANDLE_CART: [
                CallbackQueryHandler(partial_handle_cart)
            ]
        },
        fallbacks=[CommandHandler("end", end_conversation)],
        name="my_conversation",
        persistent=True,
    )
    dispatcher.add_handler(conv_handler)
    dispatcher.add_error_handler(handle_error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

    '''pic=os.path.expanduser("~/a.png")
       context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(pic,"rb"))'''
