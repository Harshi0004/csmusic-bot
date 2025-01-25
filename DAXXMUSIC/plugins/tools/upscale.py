import base64
import httpx
import os
import config
from config import BOT_USERNAME
from DAXXMUSIC import app
from pyrogram import Client, filters
import pyrogram
from uuid import uuid4
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import aiofiles, aiohttp, requests

async def image_loader(image: str, link: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as resp:
            if resp.status == 200:
                f = await aiofiles.open(image, mode="wb")
                await f.write(await resp.read())
                await f.close()
                return image
            return None

@app.on_message(filters.command("upscale", prefixes="/"))
async def upscale_image(client, message):
    chat_id = message.chat.id
    replied = message.reply_to_message
    if not replied or not replied.photo:
        return await message.reply_text("Please Reply To An Image ...")

    aux = await message.reply_text("Please Wait ...")
    image = await replied.download()

    try:
        # Use the DeepAI API to upscale the image
        response = requests.post(
            "https://api.deepai.org/api/torch-srgan",
            files={'image': open(image, 'rb')},
            headers={'api-key': '499376f8-6938-4d08-b0c0-0fd551669b7a'}
        )
        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()
        image_link = data.get("output_url")

        if image_link:
            downloaded_image = await image_loader(image, image_link)
            await aux.delete()
            if downloaded_image:
                await message.reply_document(downloaded_image)
                os.remove(downloaded_image)  # Clean up the image after sending
            else:
                await message.reply_text("Failed to download the upscaled image.")
        else:
            await aux.edit_text("Failed to get the output image link.")
    except requests.exceptions.RequestException as e:
        await aux.edit_text(f"Request failed: {str(e)}")
    except Exception as e:
        await aux.edit_text(f"An unexpected error occurred: {str(e)}")
    finally:
        if os.path.exists(image):  # Ensure the image is cleaned up
            os.remove(image)

# ------------

waifu_api_url = 'https://api.waifu.im/search'

def get_waifu_data(tags):
    params = {
        'included_tags': tags,
        'height': '>=2000'
    }
    try:
        response = requests.get(waifu_api_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching waifu data: {e}")
        return None

@app.on_message(filters.command("waifu"))
async def waifu_command(client, message):
    try:
        tags = ['maid']  # You can customize the tags as needed
        waifu_data = get_waifu_data(tags)

        if waifu_data and 'images' in waifu_data:
            first_image = waifu_data['images'][0]
            image_url = first_image['url']
            await message.reply_photo(image_url)
        else:
            await message.reply_text("No waifu found with the specified tags.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")
