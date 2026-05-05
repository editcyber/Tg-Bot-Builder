import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

# --- AYARLAR ---
API_TOKEN = '8280340805:AAFuelKEDucHd5Y94apt_Cx-v431crhKpSc'
ADMIN_ID = 6396133995  # Kenan Nasibov
ADMIN_USERNAME = "Kenan_Nasibov" # Bura öz Telegram adını ( @ işarəsiz) yaz

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# İstifadəçilərin seçdiyi dili yadda saxlamaq üçün sadə lüğət
user_langs = {}

# --- DİLLƏR VƏ MƏTNLƏR ---
STRINGS = {
    'az': {
        'welcome': "👋 <b>Botify Studio-ya xoş gəlmisiniz!</b>\n\nBiz sizin üçün 7/24 aktiv çalışan peşəkar botlar hazırlayırıq.",
        'btn_order': "🛠 Bot Sifariş Et",
        'btn_price': "💳 Qiymətlər",
        'btn_support': "📞 Adminlə Əlaqə",
        'prices': "💰 <b>Qiymətlərimiz:</b>\n\n🟢 Sadə: 25 AZN\n🟡 Orta: 45 AZN\n🔴 Mağaza: 85 AZN",
        'order_info': "Sifariş üçün ödənişi (Kapital/M10) edib, qəbzin şəklini bota göndərin.",
        'confirm_wait': "🕒 Ödənişiniz admin tərəfindən yoxlanılır...",
        'confirmed': "✅ Təbriklər! Ödəniş təsdiqləndi. Sizinlə əlaqə saxlanılacaq."
    },
    'en': {
        'welcome': "👋 <b>Welcome to Botify Studio!</b>\n\nWe create professional 24/7 bots for your business.",
        'btn_order': "🛠 Order a Bot",
        'btn_price': "💳 Prices",
        'btn_support': "📞 Contact Admin",
        'prices': "💰 <b>Prices:</b>\n\n🟢 Simple: $15\n🟡 Medium: $30\n🔴 Shop: $55",
        'order_info': "Please send the payment screenshot (Stars/KoronaPay) to start the order.",
        'confirm_wait': "🕒 Waiting for admin confirmation...",
        'confirmed': "✅ Success! Payment confirmed. We will contact you."
    },
    'ru': {
        'welcome': "👋 <b>Добро пожаловать в Botify Studio!</b>\n\nМы создаем профессиональных ботов для вашего бизнеса.",
        'btn_order': "🛠 Заказать бота",
        'btn_price': "💳 Цены",
        'btn_support': "📞 Связь с админом",
        'prices': "💰 <b>Цены:</b>\n\n🟢 Простой: 1500₽\n🟡 Средний: 3000₽\n🔴 Магазин: 5500₽",
        'order_info': "Пожалуйста, отправьте скриншот оплаты боту.",
        'confirm_wait': "🕒 Ожидайте подтверждения админом...",
        'confirmed': "✅ Оплата подтверждена! Мы свяжемся с вами."
    },
    'tr': {
        'welcome': "👋 <b>Botify Studio'ya Hoş Geldiniz!</b>\n\nİşiniz için profesyonel Telegram botları geliştiriyoruz.",
        'btn_order': "🛠 Bot Sipariş Et",
        'btn_price': "💳 Fiyatlar",
        'btn_support': "📞 Adminle İletişim",
        'prices': "💰 <b>Fiyatlarımız:</b>\n\n🟢 Basit: 500 TL\n🟡 Orta: 1000 TL\n🔴 Mağaza: 2000 TL",
        'order_info': "Lütfen ödeme dekontunu bota gönderin.",
        'confirm_wait': "🕒 Ödemeniz kontrol ediliyor...",
        'confirmed': "✅ Ödemeniz onaylandı! Sizinle iletişime geçeceğiz."
    }
}

class OrderState(StatesGroup):
    waiting_for_photo = State()

# --- KLAVİATURALAR ---
def get_main_keyboard(lang):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(STRINGS[lang]['btn_order'], STRINGS[lang]['btn_price'])
    # Adminlə əlaqə üçün ayrıca inline düymə daha peşəkar görünür
    return kb

def get_support_inline(lang):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text=STRINGS[lang]['btn_support'], url=f"https://t.me/{ADMIN_USERNAME}"))
    return kb

# --- HANDLERS ---
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("🇦🇿 Az", callback_data="setlang_az"),
        types.InlineKeyboardButton("🇬🇧 En", callback_data="setlang_en"),
        types.InlineKeyboardButton("🇷🇺 Ru", callback_data="setlang_ru"),
        types.InlineKeyboardButton("🇹🇷 Tr", callback_data="setlang_tr")
    )
    await message.answer("🌍 Choose your language / Dil seçin:", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith('setlang_'))
async def process_lang(callback: types.CallbackQuery):
    lang = callback.data.split('_')[1]
    user_langs[callback.from_user.id] = lang
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await bot.send_message(
        callback.from_user.id, 
        STRINGS[lang]['welcome'], 
        reply_markup=get_main_keyboard(lang)
    )
    # Adminlə əlaqə düyməsini inline olaraq ayrıca göndəririk
    await bot.send_message(callback.from_user.id, "⬇️", reply_markup=get_support_inline(lang))

@dp.message_handler(lambda m: any(m.text == STRINGS[l]['btn_price'] for l in STRINGS))
async def cmd_prices(message: types.Message):
    lang = user_langs.get(message.from_user.id, 'az')
    await message.answer(STRINGS[lang]['prices'])

@dp.message_handler(lambda m: any(m.text == STRINGS[l]['btn_order'] for l in STRINGS))
async def cmd_order(message: types.Message):
    lang = user_langs.get(message.from_user.id, 'az')
    await message.answer(STRINGS[lang]['order_info'])
    await OrderState.waiting_for_photo.set()

@dp.message_handler(content_types=['photo'], state=OrderState.waiting_for_photo)
async def process_payment(message: types.Message, state: FSMContext):
    lang = user_langs.get(message.from_user.id, 'az')
    
    # Adminə bildiriş
    admin_kb = types.InlineKeyboardMarkup()
    admin_kb.add(types.InlineKeyboardButton("✅ Təsdiqlə", callback_data=f"accept_{message.from_user.id}_{lang}"))
    
    await bot.send_photo(
        ADMIN_ID, 
        message.photo[-1].file_id, 
        caption=f"🔔 <b>YENİ SİFARİŞ!</b>\n\n👤 Müştəri: {message.from_user.full_name}\n🆔 ID: {message.from_user.id}\n🌐 Dil: {lang.upper()}",
        reply_markup=admin_kb
    )
    
    await message.answer(STRINGS[lang]['confirm_wait'])
    await state.finish()

@dp.callback_query_handler(lambda c: c.data.startswith('accept_'))
async def admin_accept(callback: types.CallbackQuery):
    _, user_id, lang = callback.data.split('_')
    await bot.send_message(user_id, STRINGS[lang]['confirmed'])
    await callback.message.edit_caption(caption=f"{callback.message.caption}\n\n✅ <b>TƏSDİQLƏNDİ</b>")
    await callback.answer("Müştəriyə təsdiq mesajı göndərildi!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
