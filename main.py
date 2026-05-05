import logging
import urllib.parse
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

# --- KONFİQURASİYA ---
TOKEN = '8280340805:AAFuelKEDucHd5Y94apt_Cx-v431crhKpSc'
ADMIN_ID = 6396133995
ADMIN_NICK = "gamerxx_99"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

# --- 4 DİLLİ ELİTE AGENTLİK LÜĞƏTİ ---
STRINGS = {
    'az': {
        'start': "✨ <b>Botify Studio | Next-Gen Automation</b>\n\nBiznesinizi rəqəmsal zirvəyə daşıyın. 🚀",
        'btn_services': "🚀 Xidmətlər", 'btn_support': "👨‍💻 Dəstək", 'btn_lang': "🌍 Dili Dəyiş",
        'services_text': "🛠 <b>Xidmət Kateqoriyaları:</b>",
        'info_msg': "Peşəkar xidmət təklifi üçün adminlə əlaqə saxlayın.",
        'cat_shop': "🛒 Mağaza Botu", 'cat_admin': "🛡 Qrup İdarəetmə", 'cat_game': "🎮 Oyun Mağazası",
        'order_btn': "📩 Sifariş Üçün Əlaqə", 'admin_label': "Adminlə Əlaqə",
        'support_header': "⚙️ <b>Botify Studio Dəstək</b>",
        'pre_msg': "Salam! Botify Studio-dan yazıram. Bu paketlə maraqlanıram: "
    },
    'tr': {
        'start': "✨ <b>Botify Studio | Next-Gen Automation</b>\n\nİşinizi dijital zirveye taşıyın. 🚀",
        'btn_services': "🚀 Hizmetler", 'btn_support': "👨‍💻 Destek", 'btn_lang': "🌍 Dili Değiştir",
        'services_text': "🛠 <b>Hizmet Kategorileri:</b>",
        'info_msg': "Profesyonel hizmet teklifi için adminle iletişime geçin.",
        'cat_shop': "🛒 Mağaza Botu", 'cat_admin': "🛡 Grup Yönetimi", 'cat_game': "🎮 Oyun Mağazası",
        'order_btn': "📩 Sipariş İçin İletişim", 'admin_label': "Adminle İletişim",
        'support_header': "⚙️ <b>Botify Studio Destek</b>",
        'pre_msg': "Merhaba! Botify Studio'dan yazıyorum. Bu paketle ilgileniyorum: "
    },
    'ru': {
        'start': "✨ <b>Botify Studio | Next-Gen Automation</b>\n\nПрофессиональные решения для вашего бизнеса. 🚀",
        'btn_services': "🚀 Услуги", 'btn_support': "👨‍💻 Поддержка", 'btn_lang': "🌍 Сменить язык",
        'services_text': "🛠 <b>Категории услуг:</b>",
        'info_msg': "Свяжитесь с админом для получения профессионального предложения.",
        'cat_shop': "🛒 Магазин-бот", 'cat_admin': "🛡 Управление", 'cat_game': "🎮 Игровой магазин",
        'order_btn': "📩 Связаться для заказа", 'admin_label': "Связаться с Админом",
        'support_header': "⚙️ <b>Поддержка Botify Studio</b>",
        'pre_msg': "Здравствуйте! Я из Botify Studio. Меня интересует этот пакет: "
    },
    'en': {
        'start': "✨ <b>Botify Studio | Next-Gen Automation</b>\n\nElite Telegram solutions for your business success. 🚀",
        'btn_services': "🚀 Services", 'btn_support': "👨‍💻 Support", 'btn_lang': "🌍 Change Language",
        'services_text': "🛠 <b>Service Categories:</b>",
        'info_msg': "Contact the admin for a professional service offer.",
        'cat_shop': "🛒 E-Commerce Bot", 'cat_admin': "🛡 Management", 'cat_game': "🎮 Game Store Bot",
        'order_btn': "📩 Contact to Order", 'admin_label': "Contact Admin",
        'support_header': "⚙️ <b>Botify Studio Support</b>",
        'pre_msg': "Hello! I'm from Botify Studio. I'm interested in this package: "
    }
}

# --- KLAVİATURALAR ---
def main_kb(l):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(STRINGS[l]['btn_services'])
    kb.add(STRINGS[l]['btn_support'], STRINGS[l]['btn_lang'])
    return kb

def services_kb(l):
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton(STRINGS[l]['cat_shop'], callback_data=f"inf_{l}_shop"),
        types.InlineKeyboardButton(STRINGS[l]['cat_admin'], callback_data=f"inf_{l}_admin"),
        types.InlineKeyboardButton(STRINGS[l]['cat_game'], callback_data=f"inf_{l}_game")
    )
    return kb

# --- HANDLERS ---
@dp.message_handler(commands=['start'], state="*")
async def start(m: types.Message):
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(types.InlineKeyboardButton("🇦🇿 Az", callback_data="set_az"),
           types.InlineKeyboardButton("🇹🇷 Tr", callback_data="set_tr"),
           types.InlineKeyboardButton("🇷🇺 Ru", callback_data="set_ru"),
           types.InlineKeyboardButton("🇬🇧 En", callback_data="set_en"))
    await m.answer("🌍 <b>Choose language / Dil seçin:</b>", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith('set_'))
async def set_lang(c: types.CallbackQuery):
    l = c.data.split('_')[1]
    await bot.delete_message(c.message.chat.id, c.message.message_id)
    await bot.send_message(c.from_user.id, STRINGS[l]['start'], reply_markup=main_kb(l))
    await c.answer()

@dp.message_handler(lambda m: "🚀" in m.text)
async def services(m: types.Message):
    if "Xidmətlər" in m.text: l = 'az'
    elif "Hizmetler" in m.text: l = 'tr'
    elif "Услуги" in m.text: l = 'ru'
    elif "Services" in m.text: l = 'en'
    else: l = 'az'
    await m.answer(STRINGS[l]['services_text'], reply_markup=services_kb(l))

@dp.callback_query_handler(lambda c: c.data.startswith('inf_'))
async def details(c: types.CallbackQuery):
    _, l, cat = c.data.split('_')
    names = {'shop': STRINGS[l]['cat_shop'], 'admin': STRINGS[l]['cat_admin'], 'game': STRINGS[l]['cat_game']}
    text = urllib.parse.quote(STRINGS[l]['pre_msg'] + names[cat])
    url = f"https://t.me/{ADMIN_NICK}?text={text}"
    
    kb = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(STRINGS[l]['order_btn'], url=url))
    # DÜZƏLİŞ BURA: Artıq mətndə Azərbaycan dili mətni yoxdur, STRINGS-dən götürülür
    await bot.send_message(c.from_user.id, f"📌 <b>{names[cat]}</b>\n\n{STRINGS[l]['info_msg']}", reply_markup=kb)
    await c.answer()

@dp.message_handler(lambda m: "👨‍💻" in m.text)
async def support(m: types.Message):
    if "Dəstək" in m.text: l = 'az'
    elif "Destek" in m.text: l = 'tr'
    elif "Поддержка" in m.text: l = 'ru'
    elif "Support" in m.text: l = 'en'
    else: l = 'az'
    kb = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("💬 " + STRINGS[l]['admin_label'], url=f"https://t.me/{ADMIN_NICK}"))
    await m.answer(STRINGS[l]['support_header'], reply_markup=kb)

@dp.message_handler(lambda m: "🌍" in m.text)
async def lang_change(m: types.Message):
    await start(m)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
