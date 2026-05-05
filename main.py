import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

# --- AYARLAR ---
API_TOKEN = '8280340805:AAFuelKEDucHd5Y94apt_Cx-v431crhKpSc'
ADMIN_ID = 6396133995  # Sənin ID-n

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# --- MƏTNLƏR (DİLLƏR ÜZRƏ) ---
STRINGS = {
    'az': {
        'welcome': "👋 <b>Salam! Botify Studio-ya xoş gəlmisən!</b>\n\nPeşəkar Telegram botlarının hazırlanması xidməti. 🚀",
        'menu': "🎯 Aşağıdakı menyudan birini seç:",
        'btn_order': "🛠 Bot Sifariş Et",
        'btn_price': "💳 Paketlər və Qiymətlər",
        'btn_support': "📞 Adminlə Əlaqə",
        'prices': "💰 <b>Qiymətlərimiz:</b>\n\n🟢 Sadə: 25 AZN\n🟡 Orta: 45 AZN\n🔴 Mağaza: 85 AZN\n\nÖdəniş: Kapital/M10",
        'order_msg': "Zəhmət olmasa ödəniş çekini (şəklini) bota göndərin.",
        'admin_confirm': "✅ Ödənişiniz təsdiqləndi! Tezliklə sizinlə əlaqə saxlanılacaq.",
    },
    'en': {
        'welcome': "👋 <b>Welcome to Botify Studio!</b>\n\nProfessional Telegram bot development service. 🚀",
        'menu': "🎯 Select a section from the menu:",
        'btn_order': "🛠 Order a Bot",
        'btn_price': "💳 Packages & Prices",
        'btn_support': "📞 Contact Admin",
        'prices': "💰 <b>Prices:</b>\n\n🟢 Simple: $15\n🟡 Medium: $30\n🔴 Shop: $55\n\nPayment: Telegram Stars / KoronaPay",
        'order_msg': "Please send the payment screenshot to the bot.",
        'admin_confirm': "✅ Payment confirmed! We will contact you shortly.",
    },
    # Rus və Türk dilləri də bura eyni məntiqlə əlavə olunacaq
}

# --- STATES (Mərhələlər) ---
class OrderState(StatesGroup):
    waiting_for_receipt = State()

# --- HANDLERS ---

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("🇦🇿 Az", callback_data="lang_az"),
        types.InlineKeyboardButton("🇬🇧 En", callback_data="lang_en"),
        types.InlineKeyboardButton("🇷🇺 Ru", callback_data="lang_ru"),
        types.InlineKeyboardButton("🇹🇷 Tr", callback_data="lang_tr")
    )
    await message.answer("🌍 Choose your language / Dil seçin:", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith('lang_'))
async def set_language(callback: types.CallbackQuery):
    lang = callback.data.split('_')[1]
    # Dilləri burada STRINGS-dən çəkəcəyik (Hələlik az/en aktivdir)
    l_code = lang if lang in STRINGS else 'en'
    
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(STRINGS[l_code]['btn_order'], STRINGS[l_code]['btn_price'])
    kb.add(STRINGS[l_code]['btn_support'])
    
    await bot.send_message(callback.from_user.id, STRINGS[l_code]['welcome'], reply_markup=kb)
    await callback.answer()

@dp.message_handler(lambda m: "Qiymətlər" in m.text or "Prices" in m.text)
async def show_prices(message: types.Message):
    lang = 'az' if "Qiymətlər" in message.text else 'en'
    await message.answer(STRINGS[lang]['prices'])

@dp.message_handler(lambda m: "Sifariş" in m.text or "Order" in m.text)
async def start_order(message: types.Message):
    lang = 'az' if "Sifariş" in message.text else 'en'
    await message.answer(STRINGS[lang]['order_msg'])
    await OrderState.waiting_for_receipt.set()

@dp.message_handler(content_types=['photo'], state=OrderState.waiting_for_receipt)
async def handle_receipt(message: types.Message, state: FSMContext):
    # Çeki Adminə göndər
    admin_kb = types.InlineKeyboardMarkup()
    admin_kb.add(types.InlineKeyboardButton("✅ Təsdiqlə", callback_data=f"conf_{message.from_user.id}"))
    
    await bot.send_photo(ADMIN_ID, message.photo[-1].file_id, 
                         caption=f"🔔 <b>Yeni Sifariş!</b>\nİstifadəçi: {message.from_user.full_name}\nID: {message.from_user.id}", 
                         reply_markup=admin_kb)
    
    await message.answer("🕒 Ödənişiniz yoxlanılır, zəhmət olmasa gözləyin.")
    await state.finish()

@dp.callback_query_handler(lambda c: c.data.startswith('conf_'))
async def admin_confirm(callback: types.CallbackQuery):
    user_id = callback.data.split('_')[1]
    await bot.send_message(user_id, "✅ <b>Təbriklər!</b> Ödənişiniz təsdiqləndi. Admin tezliklə sizinlə əlaqə saxlayacaq.")
    await callback.message.edit_caption("✅ Bu ödəniş təsdiqləndi.")
    await callback.answer("İstifadəçiyə bildiriş göndərildi.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
