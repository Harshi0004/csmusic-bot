import os
import time
from asyncio import sleep, gather
from pyrogram import Client, filters, enums
from DAXXMUSIC import app


# Helper function to count banned members
async def count_banned_members(app, chat_id):
    banned = 0
    async for ban in app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.BANNED):
        banned += 1
    return banned


# Helper function to count bots
async def count_bots(app, chat_id):
    bot = 0
    async for member in app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.BOTS):
        bot += 1
    return bot


# Helper function to count deleted accounts (zombies)
async def count_deleted_accounts(app, chat_id):
    deleted_acc = 0
    async for member in app.get_chat_members(chat_id):
        if member.user.is_deleted:
            deleted_acc += 1
    return deleted_acc


# Helper function to count premium users
async def count_premium_users(app, chat_id):
    premium_acc = 0
    async for member in app.get_chat_members(chat_id):
        if member.user.is_premium:
            premium_acc += 1
    return premium_acc


# Helper function to count uncached members
async def count_uncached_members(app, chat_id):
    uncached = 0
    async for member in app.get_chat_members(chat_id):
        if not member.user.is_bot and not member.user.is_deleted and not member.user.is_premium:
            uncached += 1
    return uncached


# "/groupdata" command handler
@app.on_message(~filters.private & filters.command(["groupdata"]), group=2)
async def instatus(app, message):
    start_time = time.perf_counter()
    user = await app.get_chat_member(message.chat.id, message.from_user.id)
    count = await app.get_chat_members_count(message.chat.id)

    if user.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
        sent_message = await message.reply_text("GETTING INFORMATION...")

        # Parallel data gathering
        banned, bot, deleted_acc, premium_acc, uncached = await gather(
            count_banned_members(app, message.chat.id),
            count_bots(app, message.chat.id),
            count_deleted_accounts(app, message.chat.id),
            count_premium_users(app, message.chat.id),
            count_uncached_members(app, message.chat.id)
        )

        end_time = time.perf_counter()
        timelog = "{:.2f}".format(end_time - start_time)

        # Formatting the data for better readability
        formatted_count = format_large_numbers(count)
        formatted_bots = format_large_numbers(bot)
        formatted_zombies = format_large_numbers(deleted_acc)
        formatted_banned = format_large_numbers(banned)
        formatted_premium = format_large_numbers(premium_acc)
        formatted_uncached = format_large_numbers(uncached)

        # Sending the result
        await sent_message.edit(f"""
**➖➖➖➖➖➖➖
➲ NAME : {message.chat.title} ✅
➲ MEMBERS : {formatted_count} 🫂
➖➖➖➖➖➖➖
➲ BOTS : {formatted_bots} 💡
➲ ZOMBIES : {formatted_zombies} 🧟
➲ BANNED : {formatted_banned} 🚫
➲ PREMIUM USERS : {formatted_premium} 🎁
➲ UNCACHED USERS : {formatted_uncached} 👥
➖➖➖➖➖➖➖
TIME TAKEN : {timelog} S**
""")
    else:
        sent_message = await message.reply_text("ONLY ADMINS CAN USE THIS!")
        await sleep(5)
        await sent_message.delete()


# Helper function for formatting large numbers (K, M, etc.)
def format_large_numbers(number):
    if number >= 1_000_000:
        return f"{number / 1_000_000:.1f}M"
    elif number >= 1_000:
        return f"{number / 1_000:.1f}K"
    return str(number)
