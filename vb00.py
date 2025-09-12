from telebot import *
import requests

sii_3 = telebot.TeleBot("6343519409:AAGuAOFJqCc3oWK9QoTgp-DcjMrwXW5ALCE")
darkai_state = {}

DEVELOPER_USERNAME = "@X_HXB"

def get_developer_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    developer_button = types.InlineKeyboardButton(text="المطور", url=f"https://t.me/{DEVELOPER_USERNAME.replace('@', '')}")
    markup.add(developer_button)
    return markup

@sii_3.message_handler(commands=['start'])
def start(msg):
    k = types.InlineKeyboardMarkup(row_width=1)
    b1 = types.InlineKeyboardButton(text='انشاء فيديو من نص', callback_data='text_to_video')
    b2 = types.InlineKeyboardButton(text='تحويل صورة لفيديو', callback_data='image_to_video')
    k.add(b1, b2)
    sii_3.send_message(msg.chat.id, "مرحبا بك في بوت انشاء الفيديو مع صوت 👋\n\nالتعليمات:\n- لاستخدام تحويل النص إلى فيديو: أرسل /text ثم أرسل النص الذي تريد تحويله.\n- لاستخدام تحويل الصورة إلى فيديو: أرسل /video ثم أرسل الصورة، وبعدها أرسل الوصف.\n\nيمكنك استخدام البوت في المحادثات الخاصة أو في المجموعات.", reply_markup=k)

@sii_3.message_handler(commands=['text'])
def handle_text_command(msg):
    chat_id = msg.chat.id
    darkai_state[chat_id] = {'action': 'text_to_video_command'}
    sii_3.send_message(chat_id, "أرسل النص الذي تريد تحويله إلى فيديو.", reply_markup=get_developer_markup())

@sii_3.message_handler(commands=['video'])
def handle_video_command(msg):
    chat_id = msg.chat.id
    darkai_state[chat_id] = {'action': 'image_to_video_command', 'step': 'await_image'}
    sii_3.send_message(chat_id, "أرسل الصورة التي تريد تحويلها إلى فيديو.", reply_markup=get_developer_markup())

@sii_3.callback_query_handler(func=lambda c: True)
def callback(c):
    chat_id = c.message.chat.id
    if c.data == 'text_to_video':
        darkai_state[chat_id] = {'action': 'text_to_video'}
        sii_3.edit_message_text(
            "قم بارسال الوصف من فضلك",
            chat_id=chat_id,
            message_id=c.message.message_id,
            reply_markup=get_developer_markup()
        )
    elif c.data == 'image_to_video':
        darkai_state[chat_id] = {'action': 'image_to_video', 'step': 'await_image'}
        sii_3.edit_message_text(
            "قم بارسال الصورة من فضلك",
            chat_id=chat_id,
            message_id=c.message.message_id,
            reply_markup=get_developer_markup()
        )

@sii_3.message_handler(content_types=['text', 'photo'])
def handle_message(msg):
    chat_id = msg.chat.id
    state = darkai_state.get(chat_id)

    if not state:
        sii_3.send_message(chat_id, "اضغط /start", reply_markup=get_developer_markup())
        return

    if state['action'] == 'text_to_video' and msg.content_type == 'text':
        wait_msg = sii_3.send_message(chat_id, "جارِ انشاء الفيديو ...", reply_markup=get_developer_markup())
        r = requests.get(f"https://sii3.moayman.top/api/veo3.php?text={msg.text.strip()}").json()
        video_url = r.get('video')
        if video_url:
            sii_3.send_video(chat_id, video_url, caption="الفيديو جاهز", supports_streaming=True, reply_markup=get_developer_markup())
        else:
            sii_3.send_message(chat_id, "خطأ", reply_markup=get_developer_markup())
        darkai_state.pop(chat_id)
        sii_3.delete_message(chat_id, wait_msg.message_id)

    elif state['action'] == 'text_to_video_command' and msg.content_type == 'text':
        wait_msg = sii_3.send_message(chat_id, "جارِ انشاء الفيديو ...", reply_markup=get_developer_markup())
        r = requests.get(f"https://sii3.moayman.top/api/veo3.php?text={msg.text.strip()}").json()
        video_url = r.get('video')
        if video_url:
            sii_3.send_video(chat_id, video_url, caption="الفيديو جاهز", supports_streaming=True, reply_markup=get_developer_markup())
        else:
            sii_3.send_message(chat_id, "خطأ", reply_markup=get_developer_markup())
        darkai_state.pop(chat_id)
        sii_3.delete_message(chat_id, wait_msg.message_id)

    elif state['action'] == 'image_to_video' or state['action'] == 'image_to_video_command':
        if state['step'] == 'await_image':
            if msg.content_type == 'photo':
                file_info = sii_3.get_file(msg.photo[-1].file_id)
                file_url = f"https://api.telegram.org/file/bot{sii_3.token}/{file_info.file_path}"
                darkai_state[chat_id]['image_url'] = file_url
                darkai_state[chat_id]['step'] = 'await_description'
                sii_3.send_message(chat_id, "قم بارسال الوصف من فضلك", reply_markup=get_developer_markup())
            else:
                sii_3.send_message(chat_id, "قم بارسال الصورة من فضلك", reply_markup=get_developer_markup())
        elif state['step'] == 'await_description' and msg.content_type == 'text':
            description = msg.text.strip()
            image_url = state['image_url']
            wait_msg = sii_3.send_message(chat_id, "جارِ انشاء الفيديو ...", reply_markup=get_developer_markup())
            try:
                data = {'text': description, 'link': image_url}
                r = requests.post("https://sii3.moayman.top/api/veo3.php", data=data).json()
                video_url = r.get('video')
                if video_url:
                    sii_3.send_video(chat_id, video_url, caption="تم انشاء الفيديو", supports_streaming=True, reply_markup=get_developer_markup())
                else:
                    sii_3.send_message(chat_id, "خطأ", reply_markup=get_developer_markup())
            except Exception as e:
                sii_3.send_message(chat_id, f"{e}", reply_markup=get_developer_markup())
            finally:
                darkai_state.pop(chat_id)
                sii_3.delete_message(chat_id, wait_msg.message_id)

sii_3.polling()

