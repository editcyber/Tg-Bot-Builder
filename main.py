import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
import urllib.parse

# --- KONFİQURASİYA ---
TOKEN = '8280340805:AAFuelKEDucHd5Y94apt_Cx-v431crhKpSc'
ADMIN_NICK = "gamerxx_99" # Sənin dəqiq ləqəbin

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

# --- PREMİUM MƏTNLƏR LÜĞƏTİ ---
STRINGS = {
    'az': {
        'start': "✨ <b>Botify Studio | Next-Gen Automation</b>\n\nİdeyalarınızı rəqəmsal reallığa çeviririk. Telegram ekosistemində ən sürətli və stabil həllər üçün doğru ünvandasınız. 🚀",
        'menu': "💎 <b>Xidmət Menyusu:</b>",
        'btn_services': "🚀 Bot Xidmətləri",
        'btn_support': "👨‍💻 Canlı Dəstək",
        'btn_lang': "🌍 Dili Dəyiş",
        'services_text': "🛠 <b>Hazırladığımız Bot Tipləri:</b>\n\nAşağıdakı kateqoriyalardan birini seçərək ətraflı məlumat ala və birbaşa sifariş verə bilərsiniz:",
        'cat_shop': "🛒 E-Mağaza Botları",
        'cat_admin': "🛡 Qrup/Kanal İdarəetmə",
        'cat_game': "🎮 Oyun/Top-up Mağazaları",
        'cat_custom': "🧪 Özəl Layihələr",
        'order_btn': "📩 Sifariş Üçün Adminlə Əlaqə",
        'pre_msg': "Salam! Mən Botify Studio-dan gəlirəm. Sizinlə bu paket barədə danışmaq istəyirəm: "
    },
    'en': {
        'start': "✨ <b>Botify Studio | Next-Gen Automation</b>\n\nTransforming ideas into digital reality. You are in the right place for elite Telegram solutions. 🚀",
        'menu': "💎 <b>Main Menu:</b>",
        'btn_services': "🚀 Services",
        'btn_support': "👨‍💻 Live Support",
        'btn_lang': "🌍 Change Language",
        'services_text': "🛠 <b>Our Solutions:</b>\n\nChoose a category below to get details and order directly:",
        'cat_shop': "🛒 E-Commerce Bots",
        'cat_admin': "🛡 Group/Channel Guard",
        'cat_game': "🎮 Game Store/Top-up",
        'cat_custom': "🧪 Custom Solutions",
        'order_btn': "📩 Contact Admin to Order",
        'pre_msg': "Hello! I am from Botify Studio. I want to discuss this package: "
    }
}

# --- YARDIMÇI FUNKSİYALAR ---
def get_order_link(package_name, lang):
    base_text = STRINGS[lang]['pre_msg'] + package_name
    encoded_text = urllib.parse.quote(base_text)
    return f"https://t.me/{ADMIN_NICK}?text={encoded_text}"

# --- KLAVİATURALAR ---
def main_keyboard(l):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(STRINGS[l]['btn_services'])
    kb.add(STRINGS[l]['btn_support'], STRINGS[l]['btn_lang'])
    return kb

def services_keyboard(l):
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton(STRINGS[l]['cat_shop'], callback_data=f"info_shop_{l}"),
        types.InlineKeyboardButton(STRINGS[l]['cat_admin'], callback_data=f"info_admin_{l}"),
        types.InlineKeyboardButton(STRINGS[l]['cat_game'], callback_data=f"info_game_{l}"),
        types.InlineKeyboardButton(STRINGS[l]['cat_custom'], callback_data=f"info_custom_{l}")
    )
    return kb

# --- HANDLERS ---
@dp.message_handler(commands=['start'], state="*")
async def start_cmd(message: types.Message):
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(types.InlineKeyboardButton("🇦🇿 Azərbaycan", callback_data="lang_az"),
           types.InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"))
    await message.answer("🌍 <b>Lütfən davam etmək üçün dil seçin:</b>\n<i>Please select a language to continue:</i>", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith('lang_'))
async def set_language(callback: types.CallbackQuery):
    l = callback.data.split('_')[1]
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, STRINGS[l]['start'], reply_markup=main_keyboard(l))
    await callback.answer()

@dp.message_handler(lambda m: any(x in m.text for x in ["Xidmətlər", "Services", "🚀"]))
async def show_services(message: types.Message):
    l = 'az' if "Xidmətlər" in message.text else 'en'
    await message.answer(STRINGS[l]['services_text'], reply_markup=services_keyboard(l))

@dp.callback_query_handler(lambda c: c.data.startswith('info_'))
async def show_details(callback: types.CallbackQuery):
    _, category, l = callback.data.split('_')
    
    details = {
        'shop': ("🛒 <b>E-Commerce Solutions</b>\n\n- Səbət sistemi\n- Məhsul kataloqu\n- Avtomatik sifariş bildirişi", "E-Commerce Bot"),
        'admin': ("🛡 <b>Group Defender</b>\n\n- Reklam və söyüş əleyhinə filtr\n- Yeni üzv qarşılama\n- Ban/Mute sistemi", "Group/Channel Admin Bot"),
        'game': ("🎮 <b>Game & Top-up Store</b>\n\n- Oyun içi valyuta satışı\n- Avtomatik teslimat\n- İstifadəçi balansı", "Game/Top-up Store Bot"),
        'custom': ("🧪 <b>Custom Projects</b>\n\n- Sizin ideyanız əsasında tam fərqli funksiyalar.", "Custom Project")
    }
    
    text, package_name = details[category]
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(STRINGS[l]['order_btn'], url=get_order_link(package_name, l)))
    
    await bot.send_message(callback.from_user.id, text, reply_markup=kb)
    await callback.answer()

@dp.message_handler(lambda m: any(x in m.text for x in ["Dəstək", "Support", "👨‍💻"]))
async def support_cmd(message: types.Message):
    l = 'az' if "Dəstək" in message.text else 'en'
    kb = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("💬 @"+ADMIN_NICK, url=f"https://t.me/{ADMIN_NICK}"))
    await message.answer(STRINGS[l]['btn_support'], reply_markup=kb)

@dp.message_handler(lambda m: any(x in m.text for x in ["Dili", "Language", "🌍"]))
async def change_lang(message: types.Message):
    await start_cmd(message)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
