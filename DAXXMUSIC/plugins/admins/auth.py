import logging

from pyrogram import filters
from pyrogram.types import Message
from DAXXMUSIC import app
from DAXXMUSIC.utils import extract_user, int_to_alpha
from DAXXMUSIC.utils.database import (
    delete_authuser,
    get_authuser,
    get_authuser_names,
    save_authuser,
)
from DAXXMUSIC.utils.decorators import AdminActual, language
from DAXXMUSIC.utils.inline import close_markup
from config import BANNED_USERS, adminlist


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.on_message(filters.command("auth") & filters.group & ~BANNED_USERS)
@AdminActual
async def auth(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
    
    user = await extract_user(message)
    token = await int_to_alpha(user.id)
    _check = await get_authuser_names(message.chat.id)
    count = len(_check)

    if count == 25:
        return await message.reply_text(_["auth_1"])

    if token not in _check:
        assis = {
            "auth_user_id": user.id,
            "auth_name": user.first_name,
            "admin_id": message.from_user.id,
            "admin_name": message.from_user.first_name,
        }
        get = adminlist.get(message.chat.id)
        if get:
            if user.id not in get:
                get.append(user.id)
        
        try:
            await save_authuser(message.chat.id, token, assis)
            logger.info(f"User {user.first_name} ({user.id}) authenticated by {message.from_user.first_name} ({message.from_user.id})")
            return await message.reply_text(_["auth_2"].format(user.mention))
        except Exception as e:
            logger.error(f"Error saving auth user: {str(e)}")
            return await message.reply_text("An error occurred while saving the user.")
    else:
        return await message.reply_text(_["auth_3"].format(user.mention))


@app.on_message(filters.command("unauth") & filters.group & ~BANNED_USERS)
@AdminActual
async def unauthusers(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
    
    user = await extract_user(message)
    token = await int_to_alpha(user.id)

    try:
        deleted = await delete_authuser(message.chat.id, token)
        get = adminlist.get(message.chat.id)
        if get and user.id in get:
            get.remove(user.id)
        
        if deleted:
            logger.info(f"User {user.first_name} ({user.id}) removed from auth list by {message.from_user.first_name} ({message.from_user.id})")
            return await message.reply_text(_["auth_4"].format(user.mention))
        else:
            return await message.reply_text(_["auth_5"].format(user.mention))
    except Exception as e:
        logger.error(f"Error deleting auth user: {str(e)}")
        return await message.reply_text("An error occurred while removing the user.")


@app.on_message(filters.command(["authlist", "authusers"]) & filters.group & ~BANNED_USERS)
@language
async def authusers(client, message: Message, _):
    try:
        _wtf = await get_authuser_names(message.chat.id)
        if not _wtf:
            return await message.reply_text(_["setting_4"])
        
        j = 0
        mystic = await message.reply_text(_["auth_6"])
        text = _["auth_7"].format(message.chat.title)
        
        for umm in _wtf:
            _umm = await get_authuser(message.chat.id, umm)
            user_id = _umm["auth_user_id"]
            admin_id = _umm["admin_id"]
            admin_name = _umm["admin_name"]
            
            try:
                user = (await app.get_users(user_id)).first_name
                j += 1
            except:
                continue
            
            text += f"{j}➤ {user}[<code>{user_id}</code>]\n"
            text += f"   {_['auth_8']} {admin_name}[<code>{admin_id}</code>]\n\n"
        
        await mystic.edit_text(text, reply_markup=close_markup(_))
    except Exception as e:
        logger.error(f"Error fetching auth users: {str(e)}")
        await message.reply_text("An error occurred while fetching the auth list.")
