from pyrogram import Client, filters
from DAXXMUSIC import app
from config import BOT_USERNAME


def hex_to_text(hex_string):
    try:
        # Try to decode the hex string to text
        text = bytes.fromhex(hex_string.replace(" ", "")).decode('utf-8')
        return text
    except ValueError:
        return "Invalid Hexadecimal string."
    except Exception as e:
        return f"Error decoding hex: {str(e)}"


def text_to_hex(text):
    # Convert text to hexadecimal
    hex_representation = ' '.join(format(ord(char), 'x') for char in text)
    return hex_representation


# Command handler for '/code'
@app.on_message(filters.command("code"))
def convert_text(_, message):
    if len(message.command) > 1:
        input_text = " ".join(message.command[1:])

        # Convert the input text to hex and decode the text
        hex_representation = text_to_hex(input_text)
        decoded_text = hex_to_text(hex_representation)

        # Build the response text
        response_text = f"""
𝗜𝗻𝗽𝘂𝘁 𝗧𝗲𝘅𝘁➪ {input_text}
𝗛𝗲𝘅 𝗥𝗲𝗽𝗿𝗲𝘀𝗲𝗻𝘁𝗮𝘁𝗶𝗼𝗻➪ {hex_representation}
𝗗𝗲𝗰𝗼𝗱𝗲𝗱 𝗧𝗲𝘅𝘁➪ {decoded_text}

𝗕𝗬 ➪ @{BOT_USERNAME}
        """
        message.reply_text(response_text)
    else:
        message.reply_text("Please provide text after the /code command.")

