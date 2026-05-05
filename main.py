import logging
import urllib.parse
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

# --- KONFİQURASİYA ---
TOKEN = '8280340805:AAFuelKEDucHd5Y94apt_Cx-v431crhKpSc'
ADMIN_NICK = "gamerxx_99" # Link olaraq qalır, lakin düymə mətnində görünmür

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

# --- 4 DİLLİ PREMİUM LÜĞƏT ---
STRINGS = {
    'az': {
        'start': "✨ <b>Botify Studio | Next-Gen Automation</b>\n\nPeşəkar Telegram həlləri ilə biznesinizi rəqəmsal zirvəyə daşıyın.",
        'menu': "💎 <b>Əsas Menyu:</b>",
        'btn_services': "🚀 Xidmətlər", 'btn_support': "👨‍💻 Canlı Dəstək", 'btn_lang': "🌍 Dili Dəyiş",
        'services_text': "🛠 <b>Xidmət Kateqoriyaları:</b>\n\nİstədiyiniz sahəni seçin:",
        'cat_shop': "🛒 Mağaza Botu", 'cat_admin': "🛡 Qrup İdarəetmə", 'cat_game': "🎮 Oyun Mağazası",
        'order_btn': "📩 Sifariş Üçün Əlaqə", 'admin_label': "Adminlə Əlaqə",
        'pre_msg': "Salam! Botify Studio-dan yazıram. Bu paketlə maraqlanıram: "
    },
    'tr': {
        'start': "✨ <b>Botify Studio | Next-Gen Automation</b>\n\nProfesyonel çözümlerle işinizi dijital zirveye taşıyın.",
        'menu': "💎 <b>Ana Menü:</b>",
        'btn_services': "🚀 Hizmetler", 'btn_support': "👨‍💻 Canlı Destek", 'btn_lang': "🌍 Dili Değiştir",
        'services_text': "🛠 <b>Hizmet Kategorileri:</b>\n\nİstediğiniz alanı seçin:",
        'cat_shop': "🛒 Mağaza Botu", 'cat_admin': "🛡 Grup Yönetimi", 'cat_game': "🎮 Oyun Mağazası",
        'order_btn': "📩 Sipariş İçin İletişim", 'admin_label': "Adminle İletişim",
        'pre_msg': "Merhaba! Botify Studio'dan yazıyorum. Bu paketle ilgileniyorum: "
    },
    'ru': {
        'start': "✨ <b>Botify Studio | Next-Gen Automation</b>\n\nПрофессиональные решения для вашего бизнеса.",
        'menu': "💎 <b>Главное меню:</b>",
        'btn_services': "🚀 Услуги", 'btn_support': "👨‍💻 Поддержка", 'btn_lang': "🌍 Сменить язык",
        'services_text': "🛠 <b>Категории услуг:</b>\n\nВыберите интересующую вас область:",
        'cat_shop': "🛒 Магазин-бот", 'cat_admin': "🛡 Управление", 'cat_game': "🎮 Игровой магазин",
        'order_btn': "📩 Связаться для заказа", 'admin_label': "Связаться с Админом",
        'pre_msg': "Здравствуйте! Я из Botify Studio. Меня интересует этот пакет: "
    },
    'en': {
        'start': "✨ <b>Botify Studio | Next-Gen Automation</b>\n\nElite Telegram solutions for your business success.",
        'menu': "💎 <b>Main Menu:</b>",
        'btn_services': "🚀 Services", 'btn_support': "👨‍💻 Support", 'btn_lang': "🌍 Change Language",
        'services_text': "🛠 <b>Service Categories:</b>\n\nChoose your area of interest:",
        'cat_shop': "🛒 E-Commerce Bot", 'cat_admin': "🛡 Management", 'cat_game': "🎮 Game Store Bot",
        'order_btn': "📩 Contact to Order", 'admin_label': "Contact Admin",
        'pre_msg': "Hello! I'm from Botify Studio. I'm interested in this package: "
    }
}

# --- FUNKSİYALAR ---
def main_kb(l):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(STRINGS[l]['btn_services'])
    kb.add(STRINGS[l]['btn_support'], STRINGS[l]['btn_lang'])
    return kb

def services_kb(l):
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton(STRINGS[l]['cat_shop'], callback_data=f"info_shop_{l}"),
        types.InlineKeyboardButton(STRINGS[l]['cat_admin'], callback_data=f"info_admin_{l}"),
        types.InlineKeyboardButton(STRINGS[l]['cat_game'], callback_data=f"info_game_{l}")
    )
    return kb

@dp.message_handler(commands=['start'], state="*")
async def start(m: types.Message):
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(types.InlineKeyboardButton("🇦🇿 Az", callback_data="set_az"),
           types.InlineKeyboardButton("🇹🇷 Tr", callback_data="set_tr"),
           types.InlineKeyboardButton("🇷🇺 Ru", callback_data="set_ru"),
           types.InlineKeyboardButton("🇬🇧 En", callback_data="set_en"))
    await m.answer("🌍 <b>Choose your language / Dil seçin:</b>", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith('set_'))
async def set_lang(c: types.CallbackQuery):
    l = c.data.split('_')[1]
    await bot.delete_message(c.message.chat.id, c.message.message_id)
    await bot.send_message(c.from_user.id, STRINGS[l]['start'], reply_markup=main_kb(l))

@dp.message_handler(lambda m: any(x in m.text for x in ["🚀", "Hizmetler", "Услуги", "Services"]))
async def services(m: types.Message):
    l = 'az' if "🚀" in m.text else ('tr' if "Hizmetler" in m.text else ('ru' if "Услуги" in m.text else 'en'))
    await m.answer(STRINGS[l]['services_text'], reply_markup=services_kb(l))

@dp.callback_query_handler(lambda c: c.data.startswith('info_'))
async def details(c: types.CallbackQuery):
    _, cat, l = c.data.split('_')
    names = {'shop': STRINGS[l]['cat_shop'], 'admin': STRINGS[l]['cat_admin'], 'game': STRINGS[l]['cat_game']}
    text = STRINGS[l]['pre_msg'] + names[cat]
    url = f"https://t.me/{ADMIN_NICK}?text={urllib.parse.quote(text)}"
    
    kb = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(STRINGS[l]['order_btn'], url=url))
    await bot.send_message(c.from_user.id, f"📌 <b>{names[cat]}</b>\n\nPeşəkar xidmət və qiymət təklifi üçün birbaşa adminlə əlaqə saxlayın.", reply_markup=kb)

@dp.message_handler(lambda m: any(x in m.text for x in ["👨‍💻", "Destek", "Поддержка", "Support"]))
async def support(m: types.Message):
    l = 'az' if "👨‍💻" in m.text else ('tr' if "Destek" in m.text else ('ru' if "Поддержка" in m.text else 'en'))
    kb = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("💬 " + STRINGS[l]['admin_label'], url=f"https://t.me/{ADMIN_NICK}"))
    await m.answer(f"⚙️ <b>Botify Studio Support</b>\n\n{STRINGS[l]['btn_support']}:", reply_markup=kb)

@dp.message_handler(lambda m: any(x in m.text for x in ["🌍", "Dili", "Language"]))
async def lang_change(m: types.Message):
    await start(m)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
