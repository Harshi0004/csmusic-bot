import random
from pyrogram import Client, filters, enums
from DAXXMUSIC import app
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@app.on_message(filters.command(["genpassword", 'genpw']))
async def generate_password(bot, update):
    message = await update.reply_text(text="Pʀᴏᴄᴇꜱꜱɪɴɢ..")
    
    # Define characters for the password generation
    password_characters = "abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()_+".lower()
    
    # Default complexity levels
    if len(update.command) > 1:
        try:
            # Get custom limit from user
            password_length = int(update.text.split(" ", 1)[1])
        except ValueError:
            return await message.edit_text("Invalid input. Please provide a valid number for the password length.")
    else:
        # If no custom limit, pick a random complexity level
        complexity_levels = [5, 6, 7, 8, 9, 10, 12]
        password_length = random.choice(complexity_levels)
    
    # Ensure the password length is within reasonable limits
    if password_length < 5 or password_length > 20:
        return await message.edit_text("Please choose a password length between 5 and 20 characters.")

    # Generate the password
    random_password = "".join(random.sample(password_characters, password_length))
    
    # Format the output text
    password_info = f"<b>Lɪᴍɪᴛ:</b> {password_length} \n<b>Pᴀꜱꜱᴡᴏʀᴅ: <code>{random_password}</code>"

    # Create a button for adding the bot to a group
    #button = InlineKeyboardMarkup([[InlineKeyboardButton('𝗔𝗗𝗗 𝗠𝗘', url='https://t.me/YumikooBot?startgroup=true')]])

    # Send the generated password with the button
    await message.edit_text(text=password_info, reply_markup=button, parse_mode=enums.ParseMode.HTML)
