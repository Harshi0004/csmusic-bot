import asyncio
import base64
import mimetypes
import os
from pyrogram import filters, types as t
from lexica import AsyncClient
from DAXXMUSIC import app
from lexica.constants import languageModels
from typing import Union, Tuple

# Initialize AsyncClient globally to optimize performance
client = AsyncClient()

# Use typing.Union for compatibility with Python versions < 3.10
async def ChatCompletion(prompt, model) -> Union[Tuple[str, list], str]:
    try:
        modelInfo = getattr(languageModels, model)
        output = await client.ChatCompletion(prompt, modelInfo)
        if model == "bard":
            return output['content'], output['images']
        return output['content']
    except Exception as E:
        raise Exception(f"API error: {E}")

async def geminiVision(prompt, model, images) -> Union[Tuple[str, list], str]:
    imageInfo = []
    for image in images:
        try:
            with open(image, "rb") as imageFile:
                data = base64.b64encode(imageFile.read()).decode("utf-8")
                mime_type, _ = mimetypes.guess_type(image)
                if mime_type not in ['image/png', 'image/jpg', 'image/jpeg']:
                    raise Exception(f"Invalid mime type for image: {mime_type}")
                imageInfo.append({
                    "data": data,
                    "mime_type": mime_type
                })
        except Exception as e:
            raise Exception(f"Error processing image {image}: {e}")
        finally:
            os.remove(image)  # Ensure removal even if there's an error
    payload = {"images": imageInfo}
    try:
        modelInfo = getattr(languageModels, model)
        output = await client.ChatCompletion(prompt, modelInfo, json=payload)
        return output['content']['parts'][0]['text']
    except Exception as E:
        raise Exception(f"API error: {E}")

def getMedia(message):
    """Extract Media"""
    media = message.media if message.media else message.reply_to_message.media if message.reply_to_message else None
    if media:
        if message.photo:
            media = message.photo
        elif message.document and message.document.mime_type in ['image/png', 'image/jpg', 'image/jpeg'] and message.document.file_size < 5242880:
            media = message.document
        else:
            media = None
    elif message.reply_to_message and message.reply_to_message.media:
        if message.reply_to_message.photo:
            media = message.reply_to_message.photo
        elif message.reply_to_message.document and message.reply_to_message.document.mime_type in ['image/png', 'image/jpg', 'image/jpeg'] and message.reply_to_message.document.file_size < 5242880:
            media = message.reply_to_message.document
        else:
            media = None
    return media

def getText(message):
    """Extract Text From Commands"""
    text_to_return = message.text
    if message.text is None:
        return None
    if " " in text_to_return:
        try:
            return message.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None

@app.on_message(filters.command(["gpt", "bard", "llama", "mistral", "palm", "gemini"]))
async def chatbots(_, m: t.Message):
    prompt = getText(m)
    media = getMedia(m)
    if media is not None:
        return await askAboutImage(_, m, [media], prompt)
    if prompt is None:
        return await m.reply_text("Hello, How can I assist you today?")
    model = m.command[0].lower()
    output = await ChatCompletion(prompt, model)
    if model == "bard":
        output, images = output
        if len(images) == 0:
            return await m.reply_text(output)
        media = []
        for i in images:
            media.append(t.InputMediaPhoto(i))
        media[0] = t.InputMediaPhoto(images[0], caption=output)
        await _.send_media_group(m.chat.id, media, reply_to_message_id=m.id)
        return
    await m.reply_text(output['parts'][0]['text'] if model == "gemini" else output)

async def askAboutImage(_, m: t.Message, mediaFiles: list, prompt: str):
    images = []
    for media in mediaFiles:
        try:
            image = await _.download_media(media.file_id, file_name=f'./downloads/{m.from_user.id}_ask.jpg')
            images.append(image)
        except Exception as e:
            return await m.reply_text(f"Error downloading media: {e}")
    try:
        output = await geminiVision(prompt if prompt else "What's this?", "geminiVision", images)
        await m.reply_text(output)
    except Exception as e:
        await m.reply_text(f"Error processing image: {e}")
