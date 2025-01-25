from pyrogram import Client, filters
from pyrogram.types import Message
import qrcode
from DAXXMUSIC import app
from PIL import Image
import io


# Function to create a QR code
def generate_qr_code(text):
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(fill_color="white", back_color="black")

        # Save the QR code to a bytes object to send with Pyrogram
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)  # Go to the start of the bytes object

        return img_bytes
    except Exception as e:
        print(f"Error generating QR code: {e}")
        return None


@app.on_message(filters.command("qr"))
def qr_handler(client, message: Message):
    # Extracting the text passed after the command
    command_text = message.command
    if len(command_text) > 1:
        input_text = " ".join(command_text[1:])
        
        # Check if the input text is non-empty
        if input_text.strip():
            qr_image = generate_qr_code(input_text)
            if qr_image:
                message.reply_photo(qr_image, caption="Here's your QR Code!")
            else:
                message.reply_text("There was an issue generating your QR code. Please try again later.")
        else:
            message.reply_text("Please provide valid text for the QR code. Example usage: /qr text to encode.")
    else:
        message.reply_text("Please provide the text for the QR code after the command. Example usage: /qr text to encode.")
