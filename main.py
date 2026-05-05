import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

# --- AYARLAR ---
API_TOKEN = '8280340805:AAFuelKEDucHd5Y94apt_Cx-v431crhKpSc'
ADMIN_ID = 6396133995  # Kənan Nəsibov
ADMIN_USERNAME = "Kenan_Nasibov" # Öz @istifadəçi adını dırnaq içində yaz

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# --- DİLLƏR VƏ MƏTNLƏR (PREMİUM ÜSLUB) ---
STRINGS = {
    'az': {
        'welcome': "✨ <b>Botify Studio-ya Xoş Gəlmisiniz!</b>\n\nBiznesinizi rəqəmsal dünyaya daşıyın. Peşəkar, sürətli və 7/24 aktiv Telegram botları ilə xidmətinizdəyik. 🚀",
        'btn_order': "🛠 Bot Sifariş Et",
        'btn_price': "💳 Qiymətlər",
        'btn_support': "📞 Adminlə Əlaqə",
        'prices': "💰 <b>Xidmət Paketlərimiz:</b>\n\n🟢 <b>Sadə Bot:</b> 25 AZN\n🟡 <b>Orta Səviyyə:</b> 45 AZN\n🔴 <b>Mağaza Sistemi:</b> 85 AZN\n\n<i>Ödəniş üsulları: Kapital Bank / M10</i>",
        'order_info': "🎯 <b>Sifariş üçün ödənişi edib, qəbzin (çekin) şəklini bota göndərin.</b>\n\nÖdəniş təsdiqləndikdən sonra mütəxəssisimiz sizinlə əlaqə saxlayacaq.",
        'support_msg': "👨‍💻 <b>Dəstək və suallar üçün mütəxəssisimizlə birbaşa əlaqə saxlayın:</b>",
        'confirm_wait': "🕒 <b>Məlumatlarınız göndərildi.</b> Admin tərəfindən yoxlanılır...",
        'confirmed': "✅ <b>Ödəniş təsdiqləndi!</b> Tezliklə sizinlə əlaqə saxlanılacaq."
    },
    'en': {
        'welcome': "✨ <b>Welcome to Botify Studio!</b>\n\nProfessional, fast, and 24/7 active Telegram bots for your business. 🚀",
        'btn_order': "🛠 Order a Bot",
        'btn_price': "💳 Prices",
        'btn_support': "📞 Contact Admin",
        'prices': "💰 <b>Our Packages:</b>\n\n🟢 <b>Basic:</b> $15\n🟡 <b>Intermediate:</b> $30\n🔴 <b>Shop System:</b> $55\n\n<i>Payment: Telegram Stars / KoronaPay</i>",
        'order_info': "🎯 <b>Please send the payment screenshot to proceed with your order.</b>",
        'support_msg': "👨‍💻 <b>Contact our specialist for support and questions:</b>",
        'confirm_wait': "🕒 <b>Processing...</b> Waiting for admin confirmation.",
        'confirmed': "✅ <b>Payment confirmed!</b> We will contact you shortly."
    }
    # Ru və Tr hissələri də bura eyni qayda ilə əlavə oluna bilər
}

class OrderState(StatesGroup):
    waiting_for_photo = State()

# --- KLAVİATURA ---
def get_main_keyboard(lang):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    # Üst sıra 2 düymə, alt sıra 1 geniş düymə (Dəstək üçün)
    kb.add(STRINGS[lang]['btn_order'], STRINGS[lang]['btn_price'])
    kb.add(STRINGS[lang]['btn_support'])
    return kb

def get_support_inline(lang):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="💬 Yazmağa başla", url=f"https://t.me/{ADMIN_USERNAME}"))
    return kb

# --- HANDLERS ---
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("🇦🇿 Azərbaycan", callback_data="setlang_az"),
        types.InlineKeyboardButton("🇬🇧 English", callback_data="setlang_en")
    )
    await message.answer("🌍 <b>Dil seçin / Select language:</b>", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith('setlang_'))
async def process_lang(callback: types.CallbackQuery):
    lang = callback.data.split('_')[1]
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, STRINGS[lang]['welcome'], reply_markup=get_main_keyboard(lang))
    await callback.answer()

@dp.message_handler(lambda m: any(m.text == STRINGS[l]['btn_price'] for l in STRINGS))
async def cmd_prices(message: types.Message):
    lang = 'az' if "Qiymətlər" in message.text else 'en'
    await message.answer(STRINGS[lang]['prices'])

@dp.message_handler(lambda m: any(m.text == STRINGS[l]['btn_support'] for l in STRINGS))
async def cmd_support(message: types.Message):
    lang = 'az' if "Dəstək" in message.text or "Admin" in message.text else 'en'
    await message.answer(STRINGS[lang]['support_msg'], reply_markup=get_support_inline(lang))

@dp.message_handler(lambda m: any(m.text == STRINGS[l]['btn_order'] for l in STRINGS))
async def cmd_order(message: types.Message):
    lang = 'az' if "Sifariş" in message.text else 'en'
    await message.answer(STRINGS[lang]['order_info'])
    await OrderState.waiting_for_photo.set()

@dp.message_handler(content_types=['photo'], state=OrderState.waiting_for_photo)
async def process_payment(message: types.Message, state: FSMContext):
    lang = 'az' if any(message.text == STRINGS['az'][k] for k in STRINGS['az']) else 'en' # Sadələşdirilmiş dil tapma
    
    admin_kb = types.InlineKeyboardMarkup()
    admin_kb.add(types.InlineKeyboardButton("✅ Təsdiqlə", callback_data=f"accept_{message.from_user.id}"))
    
    await bot.send_photo(
        ADMIN_ID, message.photo[-1].file_id, 
        caption=f"🔔 <b>YENİ SİFARİŞ!</b>\n👤 Müştəri: {message.from_user.full_name}\n🆔 ID: {message.from_user.id}",
        reply_markup=admin_kb
    )
    await message.answer(STRINGS['az']['confirm_wait']) # Hələlik default az
    await state.finish()

@dp.callback_query_handler(lambda c: c.data.startswith('accept_'))
async def admin_accept(callback: types.CallbackQuery):
    user_id = callback.data.split('_')[1]
    await bot.send_message(user_id, "✅ <b>Təbriklər!</b> Ödənişiniz təsdiqləndi. Admin tezliklə sizinlə əlaqə saxlayacaq.")
    await callback.message.edit_caption(caption=f"{callback.message.caption}\n\n✅ <b>TƏSDİQLƏNDİ</b>")
    await callback.answer("Təsdiqləndi!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
