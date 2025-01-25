from pyrogram import Client, filters
from DAXXMUSIC import app as app

# Helper function to handle dice rolls
async def send_game(bot, message, emoji, game_name):
    try:
        x = await bot.send_dice(message.chat.id, emoji)
        score = x.dice.value
        await message.reply_text(
            f"🎮 **{game_name}**\nHey {message.from_user.mention}, your score is: **{score}** 🎉",
            quote=True,
        )
    except Exception as e:
        await message.reply_text(f"❌ An error occurred: {str(e)}", quote=True)

# Command handlers
@app.on_message(filters.command("dice"))
async def dice(bot, message):
    await send_game(bot, message, "🎲", "Dice Game")

@app.on_message(filters.command("dart"))
async def dart(bot, message):
    await send_game(bot, message, "🎯", "Dart Game")

@app.on_message(filters.command("basket"))
async def basket(bot, message):
    await send_game(bot, message, "🏀", "Basketball Game")

@app.on_message(filters.command("jackpot"))
async def jackpot(bot, message):
    await send_game(bot, message, "🎰", "Jackpot Game")

@app.on_message(filters.command("ball"))
async def ball(bot, message):
    await send_game(bot, message, "🎳", "Bowling Game")

@app.on_message(filters.command("football"))
async def football(bot, message):
    await send_game(bot, message, "⚽", "Football Game")

# Help message for users
__help__ = """
🎮 **Play Games with Emoji Dice**:
/dice - Roll a dice 🎲
/dart - Throw a dart 🎯
/basket - Shoot a basketball 🏀
/ball - Roll a bowling ball 🎳
/football - Kick a football ⚽
/jackpot - Spin the slot machine 🎰
"""

__mod_name__ = "🎲 Games"
