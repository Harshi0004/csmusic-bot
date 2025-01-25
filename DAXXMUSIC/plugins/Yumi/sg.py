import asyncio
import random
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.raw.functions.messages import DeleteHistory

from DAXXMUSIC import userbot as us, app
from DAXXMUSIC.core.userbot import assistants

@app.on_message(filters.command("sg"))
async def sg(client: Client, message: Message):
    # Check if the command has valid arguments or is a reply
    if len(message.text.split()) < 2 and not message.reply_to_message:
        return await message.reply("Usage: /sg <username/id> or reply to a user's message")

    # Get the user ID either from the command or the replied message
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        user_id = message.text.split()[1]

    # Send a processing message
    processing_message = await message.reply("<code>Processing...</code>")

    try:
        # Try fetching the user information
        user = await client.get_users(user_id)
    except Exception:
        return await processing_message.edit("<code>Please specify a valid user!</code>")

    # List of bot names
    bots = ["sangmata_bot", "sangmata_beta_bot"]
    selected_bot = random.choice(bots)

    # Check if assistants are available and select the userbot
    if 1 in assistants:
        ubot = us.one

    try:
        # Send the user ID to the selected bot
        sent_message = await ubot.send_message(selected_bot, f"{user.id}")
        await sent_message.delete()
    except Exception as e:
        return await processing_message.edit(f"<code>Error: {str(e)}</code>")

    # Wait and fetch the message from the bot
    await asyncio.sleep(1)

    async for stalk in ubot.search_messages(sent_message.chat.id):
        if stalk.text is None:
            continue  # Skip empty messages
        elif stalk:
            await message.reply(f"{stalk.text}")
            break  # Exit after the first valid message

    # Attempt to delete chat history for the selected bot
    try:
        user_info = await ubot.resolve_peer(selected_bot)
        await ubot.send(DeleteHistory(peer=user_info, max_id=0, revoke=True))
    except Exception:
        pass  # Ignore any error during history deletion

    # Delete the processing message after completing the task
    await processing_message.delete()
