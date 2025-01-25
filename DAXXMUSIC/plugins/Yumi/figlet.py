from pyrogram import filters
import asyncio
import pyfiglet 
from random import choice
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from pyrogram.handlers import MessageHandler
from DAXXMUSIC import app

# Store user-specific text input for figlet
user_texts = {}

def figle(text):
    x = pyfiglet.FigletFont.getFonts()
    font = choice(x)
    figled = str(pyfiglet.figlet_format(text, font=font))
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="ᴄʜᴀɴɢᴇ", callback_data="figlet"),
         InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data="close_reply")]
    ])
    return figled, keyboard

@app.on_message(filters.command("figlet"))
async def echo(bot, message: Message):
    global user_texts
    try:
        text = message.text.split(' ', 1)[1]
        user_texts[message.chat.id] = text  # Store user input
    except IndexError:
        return await message.reply_text("Example:\n\n`/figlet HARSHA`")

    kul_text, keyboard = figle(text)
    await message.reply_text(f"ʜᴇʀᴇ ɪs ʏᴏᴜʀ ғɪɢʟᴇᴛ :\n<pre>{kul_text}</pre>", quote=True, reply_markup=keyboard)

@app.on_callback_query(filters.regex("figlet"))
async def figlet_handler(Client, query: CallbackQuery):
    global user_texts
    try:
        text = user_texts.get(query.message.chat.id)
        if not text:
            await query.message.edit_text("No figlet text found. Please use `/figlet <text>` first.")
            return

        kul_text, keyboard = figle(text)
        await query.message.edit_text(f"ʜᴇʀᴇ ɪs ʏᴏᴜʀ ғɪɢʟᴇᴛ :\n<pre>{kul_text}</pre>", reply_markup=keyboard)

    except Exception as e:
        await query.message.edit_text(f"An error occurred: {str(e)}")

@app.on_callback_query(filters.regex("close_reply"))
async def close_handler(Client, query: CallbackQuery):
    await query.message.delete()

__mod_name__ = "Fɪɢʟᴇᴛ"
__help__ = """
❍ /figlet*:* ᴍᴀᴋᴇs ғɪɢʟᴇᴛ ᴏғ ᴛʜᴇ ɢɪᴠᴇɴ ᴛᴇxᴛ
Example:\n\n`/figlet HARSHA`
"""
