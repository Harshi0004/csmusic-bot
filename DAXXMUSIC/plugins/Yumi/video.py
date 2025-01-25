import os
import time
import asyncio
from urllib.parse import urlparse
from pyrogram import filters
from pyrogram.types import Message
from youtubesearchpython import SearchVideos
from yt_dlp import YoutubeDL
import aiohttp
from DAXXMUSIC import app

def get_file_extension_from_url(url):
    url_path = urlparse(url).path
    basename = os.path.basename(url_path)
    return basename.split(".")[-1]

def get_text(message: Message) -> [None, str]:
    """Extract Text From Commands"""
    text_to_return = message.text
    if text_to_return and " " in text_to_return:
        return text_to_return.split(None, 1)[1]
    return None

async def fetch_thumbnail(thumbnail_url: str):
    """Fetch thumbnail asynchronously to avoid blocking the bot."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail_url) as response:
                if response.status == 200:
                    return await response.read()
    except Exception as e:
        return None

@app.on_message(filters.command(["yt", "video"]))
async def ytmusic(client, message: Message):
    urlissed = get_text(message)
    await message.delete()
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    chutiya = f"[{user_name}](tg://user?id={user_id})"

    pablo = await client.send_message(message.chat.id, f"sᴇᴀʀᴄʜɪɴɢ, ᴩʟᴇᴀsᴇ ᴡᴀɪᴛ...")

    if not urlissed:
        await pablo.edit("😴 sᴏɴɢ ɴᴏᴛ ғᴏᴜɴᴅ ᴏɴ ʏᴏᴜᴛᴜʙᴇ.\n\n» ᴍᴀʏʙᴇ ᴛᴜɴᴇ ɢᴀʟᴛɪ ʟɪᴋʜᴀ ʜᴏ, ᴩᴀᴅʜᴀɪ - ʟɪᴋʜᴀɪ ᴛᴏʜ ᴋᴀʀᴛᴀ ɴᴀʜɪ ᴛᴜ !")
        return

    # Search for the video
    search = SearchVideos(f"{urlissed}", offset=1, mode="dict", max_results=1)
    mi = search.result()
    if not mi["search_result"]:
        await pablo.edit("No videos found for your query.")
        return

    video_data = mi["search_result"][0]
    video_url = video_data["link"]
    video_title = video_data["title"]
    video_id = video_data["id"]
    video_channel = video_data["channel"]
    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
    
    # Download the thumbnail
    thumbnail = await fetch_thumbnail(thumbnail_url)
    if not thumbnail:
        thumbnail = None  # Handle if the thumbnail is not available

    # Setup options for video download
    opts = {
        "format": "best",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
        "outtmpl": "%(id)s.mp4",
        "logtostderr": False,
        "quiet": True,
    }

    try:
        # Download video
        with YoutubeDL(opts) as ytdl:
            info = ytdl.extract_info(video_url, download=True)
            video_file = f"{info['id']}.mp4"
            duration = info["duration"]

    except Exception as e:
        await pablo.edit(f"**Download failed**: `{str(e)}`")
        return

    # Prepare the caption and send the video
    caption = f"❄ **Title:** [{video_title}]({video_url})\n💫 **Channel:** {video_channel}\n✨ **Searched for:** {urlissed}\n🥀 **Requested by:** {chutiya}"
    c_time = time.time()

    await client.send_video(
        message.chat.id,
        video=open(video_file, "rb"),
        duration=duration,
        file_name=video_title,
        thumb=thumbnail,
        caption=caption,
        supports_streaming=True,
        progress_args=(pablo, c_time, f"Uploading {video_title} from YouTube...", video_file),
    )

    # Cleanup
    await pablo.delete()
    os.remove(video_file)
    if thumbnail:
        os.remove(thumbnail)
