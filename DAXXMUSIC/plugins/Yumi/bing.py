from DAXXMUSIC import app
import requests as r
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import filters

API_URL = "https://sugoi-api.vercel.app/search"

@app.on_message(filters.command("bingsearch"))
async def bing_search(michiko, message):
    try:
        # Check if a keyword is provided
        if len(message.command) == 1:
            await message.reply_text("❗ Please provide a keyword to search.")
            return

        # Extract the search keyword
        keyword = " ".join(message.command[1:]).strip()
        if not keyword:
            await message.reply_text("❗ Please provide a valid keyword to search.")
            return

        # Make the API request
        params = {"keyword": keyword}
        try:
            response = r.get(API_URL, params=params, timeout=10)
            response.raise_for_status()  # Raise an error for non-2xx responses
        except r.exceptions.RequestException as e:
            await message.reply_text(f"❌ Search failed: {str(e)}")
            return

        # Process the API response
        results = response.json()
        if not results:
            await message.reply_text("❌ No results found for your search.")
            return

        # Format the results
        message_text = "🔍 **Search Results**:\n\n"
        keyboard = []
        for idx, result in enumerate(results[:7], start=1):  # Limit to 7 results
            title = result.get("title", "No Title")
            link = result.get("link", "#")
            message_text += f"{idx}. [{title}]({link})\n"
            keyboard.append([InlineKeyboardButton(text=title, url=link)])

        # Send results with inline keyboard
        if keyboard:
            reply_markup = InlineKeyboardMarkup(keyboard)
            await message.reply_text(message_text.strip(), reply_markup=reply_markup)
        else:
            await message.reply_text("❌ No valid results to display.")

    except Exception as e:
        await message.reply_text(f"❌ An unexpected error occurred: {str(e)}")
