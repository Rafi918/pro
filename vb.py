import logging
import requests
import telebot
from telebot import types
from deep_translator import GoogleTranslator

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "7244063519:AAFa013W-Maj-jjY-6UATf1c3xRIwfL4QbY"
BOT_USERNAME = "RAFI  "

# APIs لكل النماذج
APIS = {
    "gemini": "https://sii3.moayman.top/api/gemini-dark.php?gemini-pro=",
    "wormgpt": "https://dev-pycodz-blackbox.pantheonsite.io/DEvZ44d/Hacker.php",
    "chatgpt": "https://api4dev.ir/ai/?text=",
    "gemini5": "http://api.x7m.site/apis/v2/GPT-5%20mini.php?text="
}

# صور لكل نموذج
MODEL_IMAGES = {
    "wormgpt": "https://t.me/IUEEk/17",
    "chatgpt": "https://t.me/IUEEk/19", 
    "gemini": "https://t.me/IUEEk/18",
    "gemini5": "https://t.me/IUEEk/18",  
    "default": "https://t.me/IUEEk/20"   
}

bot = telebot.TeleBot(TOKEN)

user_states = {}  # لتخزين النموذج المختار لكل مستخدم
user_languages = {}  # اللغة لكل مستخدم

# لوحة اختيار النموذج الرئيسية
def main_menu_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        types.InlineKeyboardButton("Gemini", callback_data="model_gemini"),
        types.InlineKeyboardButton("WormGPT", callback_data="model_wormgpt"),
        types.InlineKeyboardButton("ChatGPT", callback_data="model_chatgpt"),
        types.InlineKeyboardButton("Gemini 5", callback_data="model_gemini5"),
        types.InlineKeyboardButton("English 🌐", callback_data="toggle_lang"),
        types.InlineKeyboardButton("المطور 🦾", url="https://t.me/X_HXB")
    )
    return markup

# لوحة اختيار النموذج بالإنجليزية
def main_menu_keyboard_en():
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        types.InlineKeyboardButton("Gemini", callback_data="model_gemini"),
        types.InlineKeyboardButton("WormGPT", callback_data="model_wormgpt"),
        types.InlineKeyboardButton("ChatGPT", callback_data="model_chatgpt"),
        types.InlineKeyboardButton("Gemini 5", callback_data="model_gemini5"),
        types.InlineKeyboardButton("العربية 🌐", callback_data="toggle_lang"),
        types.InlineKeyboardButton("Developer 🦾", url="https://t.me/X_HXB")
    )
    return markup

@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    user_languages[user_id] = "ar"  # اللغة الافتراضية عربية
    user_states[user_id] = {"model": None}

    welcome_text = """
مرحباً بك في بوت الذكاء الاصطناعي المتقدم

يمكنك اختيار أحد النماذج التالية للبدء:

• Gemini - نموذج متقدم من جوجل  
• WormGPT - نموذج متخصص مع ترجمة  
• ChatGPT - نموذج محادثة متقدم  
• Gemini 5 - أحدث نموذج من جوجل  

اختر النموذج الذي تريد استخدامه من الأزرار أدناه 👇
"""

    try:
        bot.send_photo(
            chat_id=message.chat.id,
            photo=MODEL_IMAGES["default"],
            caption=welcome_text,
            parse_mode='Markdown',
            reply_markup=main_menu_keyboard()
        )
    except Exception as e:
        logger.error(f"Error sending photo: {e}")
        bot.reply_to(message, welcome_text, parse_mode='Markdown', reply_markup=main_menu_keyboard())

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    user_id = call.from_user.id
    lang = user_languages.get(user_id, "ar")
    
    if call.data == "toggle_lang":
        new_lang = "en" if lang == "ar" else "ar"
        user_languages[user_id] = new_lang
        
        if new_lang == "ar":
            welcome_text = """
مرحباً بك في بوت الذكاء الاصطناعي المتقدم

يمكنك اختيار أحد النماذج التالية للبدء:

• Gemini - نموذج متقدم من جوجل  
• WormGPT - نموذج متخصص مع ترجمة  
• ChatGPT - نموذج محادثة متقدم  
• Gemini 5 - أحدث نموذج من جوجل  

اختر النموذج الذي تريد استخدامه من الأزرار أدناه 👇
"""
            try:
                bot.edit_message_media(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    media=types.InputMediaPhoto(MODEL_IMAGES["default"], caption=welcome_text, parse_mode='Markdown'),
                    reply_markup=main_menu_keyboard()
                )
            except:
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text=welcome_text,
                    parse_mode='Markdown',
                    reply_markup=main_menu_keyboard()
                )
        else:
            welcome_text_en = """
Welcome to the Advanced AI Bot

You can choose one of the following models to start:

• Gemini - Advanced model from Google  
• WormGPT - Specialized model with translation  
• ChatGPT - Advanced conversation model  
• Gemini 5 - Latest model from Google  

Choose the model you want to use from the buttons below 👇
"""
            try:
                bot.edit_message_media(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    media=types.InputMediaPhoto(MODEL_IMAGES["default"], caption=welcome_text_en, parse_mode='Markdown'),
                    reply_markup=main_menu_keyboard_en()
                )
            except:
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text=welcome_text_en,
                    parse_mode='Markdown',
                    reply_markup=main_menu_keyboard_en()
                )

    # معالجة اختيار النماذج
    elif call.data.startswith("model_"):
        model_type = call.data.replace("model_", "")
        user_states[user_id] = {"model": model_type}
        
        model_names_ar = {
            "gemini": "Gemini",
            "wormgpt": "WormGPT", 
            "chatgpt": "ChatGPT",
            "gemini5": "Gemini 5"
        }
        
        model_names_en = {
            "gemini": "Gemini",
            "wormgpt": "WormGPT",
            "chatgpt": "ChatGPT", 
            "gemini5": "Gemini 5"
        }
        
        if lang == "ar":
            confirmation_text = f"✅ *تم تفعيل {model_names_ar[model_type]}*\n\nيمكنك الآن إرسال رسائلك وسأرد عليك باستخدام هذا النموذج."
            bot.answer_callback_query(call.id, f"تم اختيار {model_names_ar[model_type]} ✅")
        else:
            confirmation_text = f"✅ *{model_names_en[model_type]} activated*\n\nYou can now send your messages and I will respond using this model."
            bot.answer_callback_query(call.id, f"{model_names_en[model_type]} selected ✅")
        
        # إرسال الصورة الخاصة بالنموذج
        try:
            bot.send_photo(
                chat_id=call.message.chat.id,
                photo=MODEL_IMAGES[model_type],
                caption=confirmation_text,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Error sending model photo: {e}")
            bot.send_message(
                call.message.chat.id,
                confirmation_text,
                parse_mode='Markdown'
            )

@bot.message_handler(commands=['model', 'models'])
def model_command(message):
    user_id = message.from_user.id
    lang = user_languages.get(user_id, "ar")
    
    if lang == "ar":
        welcome_text = """
مرحباً بك في بوت الذكاء الاصطناعي المتقدم

يمكنك اختيار أحد النماذج التالية للبدء:

• Gemini - نموذج متقدم من جوجل  
• WormGPT - نموذج متخصص مع ترجمة  
• ChatGPT - نموذج محادثة متقدم  
• Gemini 5 - أحدث نموذج من جوجل  

اختر النموذج الذي تريد استخدامه من الأزرار أدناه 👇
"""
        try:
            bot.send_photo(
                chat_id=message.chat.id,
                photo=MODEL_IMAGES["default"],
                caption=welcome_text,
                parse_mode='Markdown',
                reply_markup=main_menu_keyboard()
            )
        except Exception as e:
            logger.error(f"Error sending photo: {e}")
            bot.reply_to(message, welcome_text, parse_mode='Markdown', reply_markup=main_menu_keyboard())
    else:
        welcome_text_en = """
Welcome to the Advanced AI Bot

You can choose one of the following models to start:

• Gemini - Advanced model from Google  
• WormGPT - Specialized model with translation  
• ChatGPT - Advanced conversation model  
• Gemini 5 - Latest model from Google  

Choose the model you want to use from the buttons below 👇
"""
        try:
            bot.send_photo(
                chat_id=message.chat.id,
                photo=MODEL_IMAGES["default"],
                caption=welcome_text_en,
                parse_mode='Markdown',
                reply_markup=main_menu_keyboard_en()
            )
        except Exception as e:
            logger.error(f"Error sending photo: {e}")
            bot.reply_to(message, welcome_text_en, parse_mode='Markdown', reply_markup=main_menu_keyboard_en())

@bot.message_handler(func=lambda message: True)
def handle_ai_message(message):
    user_id = message.from_user.id
    chat = message.chat
    user_text = message.text

    if not user_text:
        return

    # التحقق إذا لم يختر المستخدم نموذج
    if user_id not in user_states or not user_states[user_id]["model"]:
        lang = user_languages.get(user_id, "ar")
        if lang == "ar":
            bot.reply_to(message, "⚠️ *يرجى اختيار نموذج أولاً من خلال الأزرار أدناه*", 
                        parse_mode='Markdown', 
                        reply_markup=main_menu_keyboard())
        else:
            bot.reply_to(message, "⚠️ *Please choose a model first using the buttons below*", 
                        parse_mode='Markdown', 
                        reply_markup=main_menu_keyboard_en())
        return

    model_type = user_states[user_id]["model"]
    lang = user_languages.get(user_id, "ar")

    try:
        bot.send_chat_action(chat.id, 'typing')
        
        if model_type == "gemini":
            response = requests.post(f"{APIS['gemini']}{user_text}").json()
            reply_text = response.get("response", "❌ لم أتمكن من الحصول على رد")
            reply = f"🤖 *Gemini يجيب:*\n\n{reply_text}" if lang == "ar" else f"🤖 *Gemini responds:*\n\n{reply_text}"
            
        elif model_type == "wormgpt":
            json_data = {"text": user_text, "api_key": "PyCodz"}
            response = requests.post(APIS['wormgpt'], json=json_data, timeout=10)
            reply_text = response.text.strip()
           # الترجمة لنموذج WormGPT إذا كان الرد بالإنجليزية
            if not any(char in 'أإآبةتثجحخدذرزسشصضطظعغفقكلمنهوي' for char in reply_text):
                try:
                    translation = GoogleTranslator(source='auto', target='ar').translate(reply_text)
                    reply = f"🤖 *WormGPT يجيب:*\n\n🌐 *الرد الأصلي:*\n{reply_text}\n\n *الترجمة العربية:*\n{translation}"
                except Exception as e:
                    reply = f"🤖 *WormGPT يجيب:*\n\n{reply_text}\n\n❌ *خطأ في الترجمة:* {e}"
            else:
                reply = f"🤖 *WormGPT يجيب:*\n\n{reply_text}"
            
        elif model_type == "chatgpt":
            response = requests.get(f"{APIS['chatgpt']}{user_text}")
            reply_text = response.text.strip()
            reply = f"🤖 *ChatGPT يجيب:*\n\n{reply_text}" if lang == "ar" else f"🤖 *ChatGPT responds:*\n\n{reply_text}"
            
        elif model_type == "gemini5":
            response = requests.get(f"{APIS['gemini5']}{user_text}")
            reply_text = response.text.strip()
            reply = f"🤖 *Gemini 5 يجيب:*\n\n{reply_text}" if lang == "ar" else f"🤖 *Gemini 5 responds:*\n\n{reply_text}"
        
        if not reply_text or "❌" in reply_text:
            reply = "⚠️ لم أتمكن من الحصول على رد من الذكاء الاصطناعي" if lang == "ar" else "⚠️ Could not get response from AI"
            
    except Exception as e:
        logger.error(f"AI request error: {e}")
        reply = f"❌ حدث خطأ: {e}" if lang == "ar" else f"❌ Error: {e}"

    bot.reply_to(message, reply, parse_mode='Markdown')

if __name__ == "__main__":
    logger.info("Starting bot...")
    bot.infinity_polling()