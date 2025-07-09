import asyncio
from idlelib.iomenu import errors

from aiogram import Bot, types, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.utils.formatting import Bold, Text
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiosend import CryptoPay, TESTNET

cp = CryptoPay("42336:AAjnhyXZFsOAsf2ugIChymqf8mqQ0mYcf5m", TESTNET)
bot = Bot(
    token="7620483217:AAHeIYSRxlNxNpsn9i0rt8ffcGzm_lanftE",
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)
dp = Dispatcher()


def get_keyboard_main():
    buttons = [
        [types.InlineKeyboardButton(text="💎 Пополнить баланс", callback_data="balanceup")],
        [
            types.InlineKeyboardButton(text="👤 Профиль", callback_data="profile"),
            types.InlineKeyboardButton(text="👥 Рефералы", callback_data="referal")
        ],
        [types.InlineKeyboardButton(text="ℹ️ Info", callback_data="info")]
    ]
    keyboard_main = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard_main

def get_keyboard_profile():
    buttons = [
        [types.InlineKeyboardButton(text="💎 Пополнить баланс", callback_data="balanceup")],
        [types.InlineKeyboardButton(text="📜 История", callback_data="history")],
        [types.InlineKeyboardButton(text="👥 Рефералы", callback_data="referal")],
        [types.InlineKeyboardButton(text="🔙 Назад", callback_data="back")]
    ]
    keyboard_profile = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard_profile

def get_keyboard_history():
    buttons = [
        [types.InlineKeyboardButton(text="💎 Пополнить баланс", callback_data="balanceup")],
        [types.InlineKeyboardButton(text="👤 Профиль", callback_data="profile")],
        [types.InlineKeyboardButton(text="👥 Рефералы", callback_data="referal")],
        [types.InlineKeyboardButton(text="🔙 Назад", callback_data="back")]
    ]
    keyboard_history = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard_history

def get_keyboard_back():
    buttons = [
        [types.InlineKeyboardButton(text="🔙 Назад", callback_data="back")]
    ]
    keyboard_back = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard_back

def get_keyboard_ref():
    buttons = [
        [types.InlineKeyboardButton(text="👥 Пригласить", callback_data="newref")],
        [types.InlineKeyboardButton(text="🔙 Назад", callback_data="back")]
    ]
    keyboard_ref = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard_ref


@dp.message(Command("start"))
async def start_message(message: types.Message):
    content = Text(
        "Приветствую тебя, ",
        Bold(message.from_user.full_name),
        ". Это удобный бот для покупки Sticker Pack в Telegram \n\nС ним ты можешь моментально и автоматически покупать новые наборы стикеров и обеспечить себе здоровый сон и крепкие нервы."
    )
    await message.answer(
        **content.as_kwargs(),
        reply_markup=get_keyboard_main()
    )


@dp.message()
async def get_invoice(message: types.Message):
    try:
        if float(message.text) >= 30.00:
            invoice = await cp.create_invoice(amount=float(message.text), asset="USDT")
            await message.answer(f"pay: {invoice.bot_invoice_url}")
            invoice.poll(message=message)
        else:
            await message.answer("Сумма пополнения должна быть не менее 30 TON")
    except ValueError:
        await message.answer("Укажите сумму пополнения верно")


@cp.invoice_polling()
async def handle_payment(invoice, message):
    await message.answer(f"invoice #{invoice.invoice_id} has been paid",
        reply_markup=get_keyboard_back()
    )


@dp.callback_query(F.data == "profile")
async def send_profile(callback: types.CallbackQuery):
    await callback.message.answer(text=f"👤 Ваш профиль:\n\n{callback.from_user.full_name}\nid: {callback.from_user.id}\nБаланс: 0\nМесто в топе: 123\nОчередь: 454\nРефералы: 0\n\nСтикерпаков получено: 0",
        reply_markup=get_keyboard_profile()
    )
    await callback.answer()

@dp.callback_query(F.data == "balanceup")
async def send_balance_up(callback: types.CallbackQuery):
    await callback.message.answer(f"Укажите сумму пополнения в TON:",
        reply_markup=get_keyboard_back()
    )
    await callback.answer()

@dp.callback_query(F.data == "history")
async def send_balance_up(callback: types.CallbackQuery):
    await callback.message.answer(f"Ваша история покупок:\n\n\n\nИстория пополнений:",
        reply_markup=get_keyboard_history()
    )
    await callback.answer()

@dp.callback_query(F.data == "referal")
async def check_my_ref(callback: types.CallbackQuery):
    await callback.message.answer(f"👥 Ваши рефералы:\n\nRef1\nRef2\nRef3",
        reply_markup=get_keyboard_ref()
    )
    await callback.answer()

@dp.callback_query(F.data == "info")
async def send_balance_up(callback: types.CallbackQuery):
    await callback.message.answer(f"C помощью этого бота ты сможешь автоматически покупать новые Стикерпаки и НФТ-подарки за криптовалюту TON.\nТем самым получать их практически моментально без необходимости ожидать 21 день, в отличии от покупок за звёзды.",
        reply_markup=get_keyboard_back()
    )
    await callback.answer()

@dp.callback_query(F.data == "back")
async def start_message(callback: types.CallbackQuery):
    content = Text(
        "Приветствую тебя, ",
        Bold(callback.from_user.full_name),
        ". Это удобный бот для покупки StickerPack и NFT-gift в Telegram. \n\nС ним ты можешь моментально и автоматически покупать новые наборы стикеров и обеспечить себе здоровый сон и крепкие нервы."
    )
    await callback.message.answer(
        **content.as_kwargs(),
        reply_markup=get_keyboard_main()
    )
    await callback.answer()


async def main():
    await asyncio.gather(
        dp.start_polling(bot),
        cp.start_polling(),
    )


if __name__ == "__main__":
    asyncio.run(main())