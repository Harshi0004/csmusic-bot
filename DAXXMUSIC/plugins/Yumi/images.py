import os
import shutil
from re import findall
from bing_image_downloader import downloader
from pyrogram import Client, filters
from pyrogram.types import InputMediaPhoto, Message
from DAXXMUSIC import app

@app.on_message(filters.command(["img", "image"], prefixes=["/", "!"]))
async def google_img_search(client: Client, message: Message):
    chat_id = message.chat.id

    try:
        query = message.text.split(None, 1)[1]
    except IndexError:
        return await message.reply("Please provide an image query to search!")

    # Extract the limit from query if provided
    lim = findall(r"lim=\d+", query)
    try:
        lim = int(lim[0].replace("lim=", ""))
        query = query.replace(f"lim={lim}", "")
    except IndexError:
        lim = 5  # Default limit to 5 images

    download_dir = "downloads"

    # Check if the download directory exists, create if not
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    try:
        # Download images using the Bing Image Downloader
        downloader.download(query, limit=lim, output_dir=download_dir, adult_filter_off=True, force_replace=False, timeout=60)
        images_dir = os.path.join(download_dir, query)
        if not os.listdir(images_dir):
            raise Exception("No images were downloaded.")
        lst = [os.path.join(images_dir, img) for img in os.listdir(images_dir)][:lim]
    except Exception as e:
        return await message.reply(f"Error in downloading images: {e}")

    # Notify user that images are being scrapped
    msg = await message.reply("Scraping images...")

    count = 0
    for img in lst:
        count += 1
        await msg.edit(f"𝐘ᴇsɪᴋᴏᴏ Scrapped {count}/{len(lst)} images...")

    try:
        # Send the images to the chat
        await app.send_media_group(
            chat_id=chat_id,
            media=[InputMediaPhoto(media=img) for img in lst],
            reply_to_message_id=message.id
        )
    except Exception as e:
        await msg.delete()
        return await message.reply(f"Error in sending images: {e}")
    else:
        # Clean up after sending images
        shutil.rmtree(images_dir)
        await msg.delete()

