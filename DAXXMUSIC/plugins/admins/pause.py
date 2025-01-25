from pyrogram import filters
from pyrogram.types import Message
import logging

from DAXXMUSIC import app
from DAXXMUSIC.core.call import DAXX
from DAXXMUSIC.utils.database import is_music_playing, music_off
from DAXXMUSIC.utils.decorators import AdminRightsCheck
from DAXXMUSIC.utils.inline import close_markup
from config import BANNED_USERS


# Setup logging
logger = logging.getLogger(__name__)

@app.on_message(filters.command(["pause", "cpause"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def pause_admin(cli, message: Message, _, chat_id):
    try:
        if not await is_music_playing(chat_id):
            return await message.reply_text(_["admin_1"])

        # Pause the music
        await music_off(chat_id)
        await DAXX.pause_stream(chat_id)
        
        # Send confirmation message
        await message.reply_text(
            _["admin_2"].format(message.from_user.mention),
            reply_markup=close_markup(_)
        )
        
        # Log the action
        logger.info(f"Music paused in chat {chat_id} by {message.from_user.mention}")
    
    except Exception as e:
        logger.error(f"Error occurred while pausing music in chat {chat_id}: {e}")
        await message.reply_text("**Error while pausing the music. Please try again later.**")
