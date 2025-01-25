from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired, UserAdminInvalid, BadRequest
from DAXXMUSIC import app

# Callback handler to unpin a specific message
@app.on_callback_query(filters.regex(r"^unpin"))
async def unpin_callback(client, CallbackQuery):
    user_id = CallbackQuery.from_user.id
    chat_id = CallbackQuery.message.chat.id
    member = await app.get_chat_member(chat_id, user_id)

    # Check if the user has admin privileges and can pin messages
    if member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        if member.privileges.can_pin_messages:
            pass
        else:
            await CallbackQuery.answer("You don't have the rights to unpin messages!", show_alert=True)
            return
    else:
        await CallbackQuery.answer("You don't have the rights to unpin messages!", show_alert=True)
        return

    # Parse the message ID from the callback data
    msg_id = CallbackQuery.data.split("=")[1]
    try:
        msg_id = int(msg_id)
    except ValueError:
        # Handle the case when the callback data is 'yes' or 'no' for unpinning all messages
        if msg_id == "yes":
            await client.unpin_all_chat_messages(chat_id)
            text = "I have unpinned all the pinned messages."
        else:
            text = "I will not unpin all the messages."

        # Edit the message caption to reflect the result
        await CallbackQuery.message.edit_caption(
            text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text="Delete", callback_data="delete_btn=admin")]
            ])
        )
        return

    # If a specific message ID is provided, unpin that message
    await client.unpin_chat_message(chat_id, msg_id)
    await CallbackQuery.message.edit_caption(
        "Unpinned!", 
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text="Delete", callback_data="delete_btn=admin")]
        ])
    )


# Command handler for the /unpinall command
@app.on_message(filters.command("unpinall"))
async def unpinall_command_handler(client, message):
    chat_id = message.chat.id
    admin_id = message.from_user.id
    member = await client.get_chat_member(chat_id, admin_id)

    # Check if the user is an admin and has permission to unpin messages
    if member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        if member.privileges.can_pin_messages:
            pass
        else:
            return await message.reply_text("You don't have permission to unpin something.")
    else:
        return await message.reply_text("You don't have permission to unpin something.")
    
    # Ask the admin for confirmation before unpinning all messages
    await message.reply_text(
        "Are you sure you want to unpin all the pinned messages in this chat?",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(text="YES", callback_data="unpinall=yes"),
                InlineKeyboardButton(text="NO", callback_data="unpinall=no")
            ]
        ])
    )
