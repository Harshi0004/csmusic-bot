from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import random
import requests
from DAXXMUSIC import app 

SUPPORT_CHAT = "ALLTYPECC"

def get_wish_animation():
    try:
        api = requests.get("https://nekos.best/api/v2/happy").json()
        return api["results"][0]['url']
    except (requests.exceptions.RequestException, KeyError):
        return "https://example.com/fallback_animation.gif"  # Replace with a default/fallback animation URL

@app.on_message(filters.command("wish"))
async def wish(_, m):
    if len(m.command) < 2:
        await m.reply("ᴀᴅᴅ ᴡɪꜱʜ ʙᴀʙʏ🥀!")
        return 

    text = m.text.split(None, 1)[1]
    wish_count = random.randint(1, 100)
    wish = f"✨ ʜᴇʏ! {m.from_user.first_name}! "
    wish += f"✨ ʏᴏᴜʀ ᴡɪꜱʜ: {text} "
    wish += f"✨ ᴘᴏꜱꜱɪʙʟᴇ ᴛᴏ: {wish_count}%"
    
    animation_url = get_wish_animation()
    
    await app.send_animation(
        chat_id=m.chat.id,
        animation=animation_url,
        caption=wish,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("ꜱᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT}")]]
        )
    )

BUTTON = [[InlineKeyboardButton("ꜱᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT}")]]
CUTIE = "https://64.media.tumblr.com/d701f53eb5681e87a957a547980371d2/tumblr_nbjmdrQyje1qa94xto1_500.gif"

@app.on_message(filters.command("cute"))
async def cute(_, message):
    if not message.reply_to_message:
        user_id = message.from_user.id
        user_name = message.from_user.first_name
    else:
        user_id = message.reply_to_message.from_user.id
        user_name = message.reply_to_message.from_user.first_name

    mention = f"[{user_name}](tg://user?id={str(user_id)})"
    mm = random.randint(1, 100)
    CUTE = f"🍑 {mention} {mm}% ᴄᴜᴛᴇ ʙᴀʙʏ🥀"

    await app.send_document(
        chat_id=message.chat.id,
        document=CUTIE,
        caption=CUTE,
        reply_markup=InlineKeyboardMarkup(BUTTON),
        reply_to_message_id=message.reply_to_message.message_id if message.reply_to_message else None,
    )
    
help_text = """
» ᴡʜᴀᴛ ɪꜱ ᴛʜɪꜱ (ᴡɪꜱʜ):
ʏᴏᴜ ʜᴀᴠɪɴɢ ᴀɴʏ ᴋɪɴᴅ ᴏꜰ 
(ᴡɪꜱʜᴇꜱ) ʏᴏᴜ ᴄᴀɴ ᴜꜱɪɴɢ ᴛʜɪꜱ ʙᴏᴛ ᴛᴏ ʜᴏᴡ ᴘᴏꜱꜱɪʙʟᴇ ᴛᴏ ʏᴏᴜʀ ᴡɪꜱʜ!
ᴇxᴀᴍᴘʟᴇ:» /wish : ɪ ᴡᴀɴᴛ ᴄʟᴀꜱꜱ ᴛᴏᴘᴘᴇʀ 
» /wish : ɪ ᴡᴀɴᴛ ᴀ ɴᴇᴡ ɪᴘʜᴏɴᴇ 
» /cute : ʜᴏᴡ ᴍᴜᴄʜ ɪ ᴀᴍ ᴄᴜᴛᴇ 
"""
