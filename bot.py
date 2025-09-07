import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Токен бота (вставь свой!)
BOT_TOKEN = "7619623685:AAGvQJSzN9gIGJflsqNyV2CDijdYczhxh14"

# Адрес твоего TON-кошелька (казначейский)
WALLET_ADDRESS = "UQAtOwZBJX-V_0tJHXwOXrOI-7I7T6EJ21UOk4TShQenh1os"

# ID канала, на который нужно подписаться (например, @viktor_news)
REQUIRED_CHANNEL = "@viktor_news"

# Награда за задание
REWARD_AMOUNT = "0.01"

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Команда /start
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    # Кнопка "Проверить подписку"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Проверить подписку", callback_data="check_sub")]
    ])

    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        f"Подпишись на канал {REQUIRED_CHANNEL}, затем нажми кнопку ниже — и получи {REWARD_AMOUNT} TON на свой кошелёк!",
        reply_markup=keyboard
    )

# Обработка нажатия кнопки
@dp.callback_query(lambda c: c.data == "check_sub")
async def check_subscription(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    try:
        # Проверяем, подписан ли пользователь на канал
        chat_member = await bot.get_chat_member(REQUIRED_CHANNEL, user_id)
        if chat_member.status in ["member", "administrator", "creator"]:
            # Генерируем ссылку на перевод TON
            ton_link = f"https://t.me/wallet?startattach=transfer&address={WALLET_ADDRESS}&amount={int(float(REWARD_AMOUNT) * 10**9)}&text=Reward+for+subscription"
            await callback_query.message.answer(
                f"🎉 Поздравляю! Ты подписан!\n\n"
                f"Нажми на кнопку ниже, чтобы получить {REWARD_AMOUNT} TON:\n\n"
                f"🔗 [Получить {REWARD_AMOUNT} TON]({ton_link})",
                parse_mode="Markdown",
                disable_web_page_preview=False
            )
        else:
            await callback_query.answer("❌ Ты не подписан на канал. Подпишись и попробуй снова!", show_alert=True)
    except Exception as e:
        await callback_query.answer("⚠️ Ошибка. Убедись, что канал существует и бот в нём админ.", show_alert=True)

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
