import logging
from pyrogram.types import Message
from youtube_search import YoutubeSearch
from DAXXMUSIC import app
from pyrogram import filters
from config import BOT_USERNAME

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.on_message(filters.command("search"))
async def ytsearch(_, message: Message):
    try:
        # Check if query argument is provided
        if len(message.command) < 2:
            await message.reply_text("/search needs an argument!")
            return
        
        query = message.text.split(None, 1)[1]
        m = await message.reply_text("Searching...")

        # Perform YouTube search with the query
        results = YoutubeSearch(query, max_results=5).to_dict()

        # Check if results are empty
        if not results:
            await m.edit("No results found!")
            return

        # Format search results into a string
        text = ""
        for result in results:
            text += (
                f"**Title**: {result['title']}\n"
                f"**Duration**: {result['duration']}\n"
                f"**Views**: {result['views']}\n"
                f"**Channel**: {result['channel']}\n"
                f"**Link**: [Watch here](https://www.youtube.com{result['url_suffix']})\n\n"
            )

        # Send the results
        await m.edit(text, disable_web_page_preview=True)
    
    except Exception as e:
        # Log the exception for debugging purposes
        logger.error(f"Error while processing search query: {str(e)}")
        
        # Notify the user about the error
        await m.edit("An error occurred while processing your request. Please try again later.")
