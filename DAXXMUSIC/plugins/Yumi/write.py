from pyrogram import filters
from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from datetime import datetime
import requests
from config import BOT_USERNAME
from DAXXMUSIC import app

@app.on_message(filters.command("write"))
async def handwrite(_, message: Message):
    if message.reply_to_message:
        text = message.reply_to_message.text
    else:
        text = message.text.split(None, 1)[1]
    
    # Handle long text (you can adjust the length based on the API's limits)
    if len(text) > 200:
        await message.reply_text("Text is too long. Please shorten it.")
        return

    m = await message.reply_text("Please wait...,\n\nWriting your text...")

    try:
        # Request to the API
        response = requests.get(f"https://apis.xditya.me/write?text={text}")
        write = response.url  # API might directly return a URL of the generated image

        caption = f"""
        sᴜᴄᴇssғᴜʟʟʏ ᴡʀɪᴛᴛᴇɴ ᴛᴇxᴛ 💘
        ✨ ᴡʀɪᴛᴛᴇɴ ʙʏ : [𝐘ᴜᴍɪᴋᴏᴏ](https://t.me/{BOT_USERNAME})
        🥀 ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ : {message.from_user.mention}
        """
        await m.delete()
        await message.reply_photo(photo=write, caption=caption)
    except Exception as e:
        await m.delete()
        await message.reply_text(f"Failed to generate text image. Error: {str(e)}")

mod_name = "WʀɪᴛᴇTᴏᴏʟ"

help = """
 ᴡʀɪᴛᴇs ᴛʜᴇ ɢɪᴠᴇɴ ᴛᴇxᴛ ᴏɴ ᴡʜɪᴛᴇ ᴘᴀɢᴇ ᴡɪᴛʜ ᴀ ᴘᴇɴ 🖊

❍ /write <ᴛᴇxᴛ> *:* ᴡʀɪᴛᴇs ᴛʜᴇ ɢɪᴠᴇɴ ᴛᴇxᴛ.
"""

@app.on_message(filters.command("day"))
def date_to_day_command(client: Client, message: Message):
    try:
        command_parts = message.text.split(" ", 1)
        if len(command_parts) == 2:
            input_date = command_parts[1].strip()
            try:
                date_object = datetime.strptime(input_date, "%Y-%m-%d")
                day_of_week = date_object.strftime("%A")
                message.reply_text(f"The day of the week for {input_date} is {day_of_week}.")
            except ValueError:
                message.reply_text("Invalid date format. Please use YYYY-MM-DD (e.g., 2025-01-25).")
        else:
            message.reply_text("Please provide a valid date in the format `/day YYYY-MM-DD`.")

    except ValueError as e:
        message.reply_text(f"Error: {str(e)}")
