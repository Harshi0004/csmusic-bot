from pyrogram import Client, filters
import requests, random
from bs4 import BeautifulSoup
import os, yt_dlp
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from DAXXMUSIC import app

# Define a dictionary to store video links
vdo_link = {}

# Create Inline Keyboard for interactions
keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("⊝ ᴄʟᴏsᴇ ⊝", callback_data="close_data"), InlineKeyboardButton("⊝ ᴠᴘʟᴀʏ⊝", callback_data="play")]
])

# Utility function to download the video
async def get_video_stream(link):
    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "geo_bypass": True,
        "nocheckcertificate": True,
        "quiet": True,
        "no_warnings": True,
    }
    x = yt_dlp.YoutubeDL(ydl_opts)
    try:
        info = x.extract_info(link, False)
        video_path = os.path.join("downloads", f"{info['id']}.{info['ext']}")
        if not os.path.exists(video_path):
            x.download([link])
        return video_path
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None

# Fetch video info from xnxx or other sources
def get_video_info(title):
    url_base = f'https://www.xnxx.com/search/{title}'
    try:
        with requests.Session() as s:
            r = s.get(url_base)
            soup = BeautifulSoup(r.text, "html.parser")
            video_list = soup.findAll('div', attrs={'class': 'thumb-block'})
            if video_list:
                random_video = random.choice(video_list)
                thumbnail = random_video.find('div', class_="thumb").find('img').get("src")
                if thumbnail:
                    # Adjust thumbnail size
                    thumbnail_500 = thumbnail.replace('/h', '/m').replace('/1.jpg', '/3.jpg')
                    link = random_video.find('div', class_="thumb-under").find('a').get("href")
                    if link and 'https://' not in link:
                        return {'link': 'https://www.xnxx.com' + link, 'thumbnail': thumbnail_500}
    except Exception as e:
        print(f"Error: {e}")
    return None

# Command to fetch and send random video
@app.on_message(filters.command("porn"))
async def get_random_video_info(client, message):
    if len(message.command) < 2:
        await message.reply("Please provide a title to search.")
        return

    title = ' '.join(message.command[1:])
    video_info = get_video_info(title)
    
    if video_info:
        video_link = video_info['link']
        video = await get_video_stream(video_link)
        if video:
            vdo_link[message.chat.id] = {'link': video_link}
            keyboard1 = InlineKeyboardMarkup([
                [InlineKeyboardButton("⊝ ᴄʟᴏsᴇ ⊝", callback_data="close_data"), InlineKeyboardButton("⊝ ᴠᴘʟᴀʏ⊝", callback_data="vplay")]
            ])
            await message.reply_video(video, caption=f"{title}", reply_markup=keyboard1)
        else:
            await message.reply("Error downloading video.")
    else:
        await message.reply(f"No video link found for '{title}'.")

# Command to fetch video from xnxx
@app.on_message(filters.command("xnxx"))
async def get_random_video_xnxx(client, message):
    if len(message.command) < 2:
        await message.reply("Please provide a title to search.")
        return

    title = ' '.join(message.command[1:])
    video_info = get_video_info(title)
    
    if video_info:
        video_link = video_info['link']
        video = await get_video_stream(video_link)
        if video:
            # Add additional info (e.g., views, ratings)
            views = "N/A"  # Placeholder - replace with actual API call or logic to fetch views
            ratings = "N/A"  # Placeholder - replace with actual API call or logic to fetch ratings
            
            await message.reply_video(
                video,
                caption=f"Title: {title}\nViews: {views}\nRatings: {ratings}",
                reply_markup=keyboard
            )
        else:
            await message.reply("Error downloading video.")
    else:
        await message.reply(f"No video link found for '{title}'.")

# Handle play callback
@app.on_callback_query(filters.regex("^play"))
async def play_callback(_, query):
    # You can add more logic here before initiating playback
    await play(query.from_user.id)  # Assuming play function accepts user ID
    await query.answer("Playback started!")

# Handle close callback
@app.on_callback_query(filters.regex("^close_data"))
async def close_callback(_, query):
    chat_id = query.message.chat.id
    await query.message.delete()
