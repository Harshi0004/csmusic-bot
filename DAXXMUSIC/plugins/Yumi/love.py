from pyrogram import Client, filters
import random
from DAXXMUSIC import app

def get_random_message(love_percentage):
    """Generate a message based on love percentage."""
    if love_percentage <= 30:
        return random.choice([
            "Love is in the air, but it's a bit shy. Maybe try again later? 😅",
            "A good start, but there's a lot of room to grow! 🌱",
            "It’s the beginning, but keep working on it! 💪"
        ])
    elif love_percentage <= 70:
        return random.choice([
            "A strong connection is forming. Keep the spark alive! 🔥",
            "Things are looking good! Keep nurturing the relationship. 💕",
            "Love is blossoming, but don’t take it for granted! 🌸"
        ])
    else:
        return random.choice([
            "Wow! A perfect match! 💖",
            "You two are meant to be together! ❤️‍🔥",
            "It’s destiny! A love story for the ages! 📖💫"
        ])

@app.on_message(filters.command("love", prefixes="/"))
def love_command(client, message):
    """Handles the /love command."""
    command, *args = message.text.split(" ")

    # Ensure two names are provided
    if len(args) < 2:
        return app.send_message(message.chat.id, "Please enter two names after the command, like this: `/love Alice Bob`.")

    name1 = args[0].strip()
    name2 = args[1].strip()

    # Validate the names (ensure they are not empty)
    if not name1 or not name2:
        return app.send_message(message.chat.id, "Both names must be non-empty!")

    # Generate a random love percentage
    love_percentage = random.randint(10, 100)
    love_message = get_random_message(love_percentage)

    # Construct and send the response
    response = f"{name1} 💕 + {name2} 💕 = {love_percentage}%\n\n{love_message}"
    app.send_message(message.chat.id, response)
