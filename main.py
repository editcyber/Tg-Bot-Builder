import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

# --- KONFİQURASİYA ---
TOKEN = '8280340805:AAFuelKEDucHd5Y94apt_Cx-v431crhKpSc'
ADMIN_ID = 6396133995
ADMIN_NICK = "gamerxx_99" # Artıq düzgün ləqəb qeyd olundu!

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

# --- MULTI-LANGUAGE DB ---
STRINGS = {
    'az': {
        'start': "💎 <b>Botify Studio-ya Xoş Gəlmisiniz!</b>\n\nTelegram ekosistemində ən peşəkar və avtomatlaşdırılmış həlləri təqdim edirik. Sizin biznesiniz, bizim kodumuz. ✨",
        'menu': "💎 <b>Əsas Menyu:</b>",
        'btn_services': "🚀 Xidmətlər", 'btn_prices': "💳 Tariflər", 'btn_support': "👨‍💻 Mütəxəssis Dəstəyi", 'btn_lang': "🌍 Dili Dəyiş",
        'prices': "📊 <b>Xidmət Paketlərimiz:</b>\n\n📦 <b>Essential:</b> 25 AZN\n⚡ <b>Professional:</b> 55 AZN\n👑 <b>Enterprise:</b> 95 AZN\n\n<i>Ödəniş: Kapital Bank / M10</i>",
        'order_step1': "📸 <b>Sifariş üçün ödəniş çekini bota göndərin:</b>",
        'pending': "⏳ <b>Məlumatlarınız mərkəzi sistemə göndərildi.</b> Admin təsdiqi gözlənilir.",
        'done': "✅ <b>Təbriklər!</b> Ödəniş təsdiqləndi. İşi təhvil vermək üçün admin sizinlə əlaqə saxlayacaq."
    },
    'en': {
        'start': "💎 <b>Welcome to Botify Studio!</b>\n\nProviding elite automation solutions for the Telegram ecosystem. ✨",
        'menu': "💎 <b>Main Menu:</b>",
        'btn_services': "🚀 Services", 'btn_prices': "💳 Pricing", 'btn_support': "👨‍💻 Expert Support", 'btn_lang': "🌍 Language",
        'prices': "📊 <b>Our Packages:</b>\n\n📦 <b>Essential:</b> $15\n⚡ <b>Professional:</b> $35\n👑 <b>Enterprise:</b> $65\n\n<i>Payment: Crypto / Stars</i>",
        'order_step1': "📸 <b>Send your payment receipt to proceed:</b>",
        'pending': "⏳ <b>Data transmitted.</b> Awaiting admin verification.",
        'done': "✅ <b>Success!</b> Payment verified. We will contact you shortly."
    }
}

class SystemStates(StatesGroup):
    lang = State()
    order = State()

# --- KEYBOARDS ---
def main_kb(l):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(STRINGS[l]['btn_services'], STRINGS[l]['btn_prices'])
    kb.add(STRINGS[l]['btn_support'], STRINGS[l]['btn_lang'])
    return kb

def support_kb(l):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="💬 @"+ADMIN_NICK, url=f"https://t.me/{ADMIN_NICK}"))
    return kb

# --- HANDLERS ---
@dp.message_handler(commands=['start'], state="*")
async def start(m: types.Message):
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(types.InlineKeyboardButton("🇦🇿 Azərbaycan", callback_data="set_az"),
           types.InlineKeyboardButton("🇬🇧 English", callback_data="set_en"))
    await m.answer("🌍 <b>Choose your language / Dil seçin:</b>", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith('set_'), state="*")
async def set_lang(c: types.CallbackQuery, state: FSMContext):
    l = c.data.split('_')[1]
    await state.update_data(lang=l)
    await bot.delete_message(c.message.chat.id, c.message.message_id)
    await bot.send_message(c.from_user.id, STRINGS[l]['start'], reply_markup=main_kb(l))
    await c.answer()

@dp.message_handler(lambda m: any(x in m.text for x in ["Tariflər", "Pricing", "💳"]))
async def prices(m: types.Message, state: FSMContext):
    data = await state.get_data()
    l = data.get('lang', 'az')
    await m.answer(STRINGS[l]['prices'])

@dp.message_handler(lambda m: any(x in m.text for x in ["Dəstək", "Support", "👨‍💻"]))
async def support(m: types.Message, state: FSMContext):
    data = await state.get_data()
    l = data.get('lang', 'az')
    await m.answer("👨‍💻 <b>Direct Contact:</b>", reply_markup=support_kb(l))

@dp.message_handler(lambda m: any(x in m.text for x in ["Xidmətlər", "Services", "🚀"]))
async def services(m: types.Message, state: FSMContext):
    data = await state.get_data()
    l = data.get('lang', 'az')
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(types.InlineKeyboardButton("🛒 E-Commerce Bot", callback_data="order_init"),
           types.InlineKeyboardButton("🛡️ Group Defender", callback_data="order_init"),
           types.InlineKeyboardButton("🎮 Game Store Bot", callback_data="order_init"))
    await m.answer("🚀 <b>Available Solutions:</b>", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data == "order_init")
async def order_start(c: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    l = data.get('lang', 'az')
    await SystemStates.order.set()
    await bot.send_message(c.from_user.id, STRINGS[l]['order_step1'])
    await c.answer()

@dp.message_handler(content_types=['photo'], state=SystemStates.order)
async def process_order(m: types.Message, state: FSMContext):
    data = await state.get_data()
    l = data.get('lang', 'az')
    admin_btn = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("✅ Approve", callback_data=f"ok_{m.from_user.id}"))
    await bot.send_photo(ADMIN_ID, m.photo[-1].file_id, 
                         caption=f"🔥 <b>NEW ORDER</b>\n\nUser: {m.from_user.full_name}\nID: {m.from_user.id}\nLang: {l}",
                         reply_markup=admin_btn)
    await m.answer(STRINGS[l]['pending'])
    await state.finish()

@dp.callback_query_handler(lambda c: c.data.startswith('ok_'))
async def approve(c: types.CallbackQuery):
    uid = c.data.split('_')[1]
    await bot.send_message(uid, "✅ <b>Order Approved!</b> We will contact you shortly.")
    await c.message.edit_caption("✅ Approved")
    await c.answer("Notified.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
