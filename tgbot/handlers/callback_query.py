import logging

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot.db.queries import Database
from tgbot.db.redis_db import get_redis
from tgbot.keyboards.inline import product_inline_kb, shopping_cart_clean_kb
from tgbot.keyboards.reply import generate_product_keyboard, generate_category_keyboard, menu_keyboards
from tgbot.misc.i18n import i18ns
from tgbot.misc.states import BuyState
from tgbot.misc.utils import get_shopping_cart

_ = i18ns.gettext


async def increase_count(callback_query: CallbackQuery):
    # Increase count logic here

    _increase, count, product_id = callback_query.data.split('_')
    count = int(count) + 1
    await callback_query.message.edit_reply_markup(
        reply_markup=product_inline_kb(product_id, count)
    )
    await callback_query.answer(_("{count} ta").format(count=count))


async def decrease_count(callback_query: CallbackQuery):
    # Decrease count logic here
    _decrease, count, product_id = callback_query.data.split('_')
    if count != "1":
        count = int(count) - 1
        await callback_query.message.edit_reply_markup(
            reply_markup=product_inline_kb(product_id, count)
        )
    await callback_query.answer(_("{count} ta").format(count=count))


async def show_count(callback_query: CallbackQuery):
    # Show count logic here
    await callback_query.answer(_("ta"))


async def add_to_cart(callback_query: CallbackQuery, state: FSMContext, user_lang, db: Database):
    # Add to cart logic here
    _cart, count, product_id = callback_query.data.split('_')
    await callback_query.answer("Added to cart")
    await callback_query.message.edit_caption(_("Qo'shildi: {count} ta").format(count=count))
    redis = await get_redis()
    key = f"shopping_cart:{callback_query.from_user.id}"

    data = await state.get_data()
    category = data.get("category")
    try:
        item_key = f"{data['product']}:{count}"
        await redis.hset(key, item_key, data['price'])
    except Exception as _e:  # noqa
        await callback_query.message.answer(_("Server bilan ulanishda muammo bo'ldi. Boshidan uruning"))
    if category:
        products = await db.get_products(category=category, user_lang=user_lang)
        await callback_query.message.answer(_("Muzqaymoqni tanlang"),
                                            reply_markup=generate_category_keyboard(products, user_lang))
        await BuyState.get_product.set()
    else:
        categories = await db.get_categories()
        await callback_query.message.answer(_("Muzqaymoq turini tanlang."),
                                            reply_markup=generate_category_keyboard(categories, user_lang))
        await BuyState.get_category.set()


async def buy_cart(callback_query: CallbackQuery):
    # Show count logic here
    # TODO: integrations phone getting and billing
    await callback_query.answer(_("ta"))


async def close_cart(callback_query: CallbackQuery):
    # Show count logic here
    await callback_query.answer(_("Davom eting"))
    await callback_query.message.delete()


async def clean_cart(callback_query: CallbackQuery):
    # Show count logic here
    await callback_query.answer(_("Javob bering"))
    await callback_query.message.edit_text(text=_("Rostdan ham savatni tozalamoqchimisiz?"),
                                           reply_markup=shopping_cart_clean_kb())


async def yes_clean(callback_query: CallbackQuery):
    redis = await get_redis()
    key = f"shopping_cart:{callback_query.from_user.id}"

    # Delete the entire cart from Redis
    await redis.delete(key)
    await callback_query.answer(_("Tozalandi"))
    await callback_query.message.delete()
    await callback_query.message.answer(_("📍 Geolokatsiyani yuboring yoki yetkazib berish manzilini tanlang"),
                                           reply_markup=menu_keyboards())
    await BuyState.get_location.set()


async def no_clean(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.delete()
    await get_shopping_cart(callback_query.message)


def register_callback(dp: Dispatcher):
    dp.register_callback_query_handler(increase_count,
                                       lambda c: c.data.startswith('increase'),
                                       state="*")
    dp.register_callback_query_handler(decrease_count,
                                       lambda c: c.data.startswith('decrease'),
                                       state="*")
    dp.register_callback_query_handler(show_count,
                                       lambda c: c.data == 'count',
                                       state="*")
    dp.register_callback_query_handler(add_to_cart,
                                       lambda c: c.data.startswith('addtocart'),
                                       state="*")
    dp.register_callback_query_handler(close_cart,
                                       lambda c: c.data.startswith('close'),
                                       state="*")
    dp.register_callback_query_handler(clean_cart,
                                       lambda c: c.data.startswith('clean_trash'),
                                       state="*")
    dp.register_callback_query_handler(buy_cart,
                                       lambda c: c.data.startswith('buy'),
                                       state="*")
    dp.register_callback_query_handler(yes_clean,
                                       lambda c: c.data == 'yes',
                                       state="*")
    dp.register_callback_query_handler(no_clean,
                                       lambda c: c.data == 'no',
                                       state="*")