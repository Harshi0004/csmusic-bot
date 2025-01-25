import aiohttp
from pyrogram import Client, filters
from DAXXMUSIC import app

@app.on_message(filters.command("weather"))
async def weather(client, message):
    try:
        # Get the location from user message
        user_input = message.command[1]
        location = user_input.strip()
        
        # URL for fetching weather data as an image
        weather_url = f"https://wttr.in/{location}.png"

        # Use aiohttp to check if the weather URL exists and fetch the image
        async with aiohttp.ClientSession() as session:
            async with session.get(weather_url) as response:
                if response.status == 200:
                    # Reply with the weather information as a photo
                    await message.reply_photo(photo=weather_url, caption=f"Here's the weather for {location}")
                else:
                    # If the location is invalid or no image is returned
                    await message.reply_text(f"Couldn't fetch the weather for {location}. Please check the location and try again.")
    except IndexError:
        # User didn't provide a location
        await message.reply_text("Please provide a location. Example: /weather NEW YORK")
    except Exception as e:
        # Handle unexpected errors
        await message.reply_text(f"An error occurred: {str(e)}")
