from pyrogram import Client, filters
import requests
from DAXXMUSIC import app

# Define a command handler for the /meme command
@app.on_message(filters.command("meme"))
def meme_command(client, message):
    """Handles the /meme command."""
    # API endpoint for random memes
    api_url = "https://meme-api.com/gimme"

    try:
        # Make a request to the API
        response = requests.get(api_url)

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            data = response.json()

            # Extract meme URL and title
            meme_url = data.get("url")
            title = data.get("title")

            # Check if the data contains the necessary fields
            if meme_url and title:
                # Mention the bot username in the caption
                caption = f"{title}\n\nRequested by {message.from_user.mention}\nBot username: @{app.get_me().username}"

                # Send the meme image to the user with the modified caption
                message.reply_photo(
                    photo=meme_url,
                    caption=caption
                )
            else:
                message.reply_text("Sorry, the meme API didn't provide valid data. Please try again later.")
        else:
            message.reply_text(f"Failed to fetch meme. API responded with status code: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        # Handle any request-related errors (timeouts, connectivity issues, etc.)
        print(f"Error fetching meme: {e}")
        message.reply_text("Sorry, I couldn't fetch a meme at the moment due to a network issue.")
    
    except Exception as e:
        # General exception handling
        print(f"Unexpected error: {e}")
        message.reply_text("Something went wrong. Please try again later.")
