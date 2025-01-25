import requests
from bs4 import BeautifulSoup as BSP
from DAXXMUSIC import app as DAXX
from pyrogram import filters

url = "https://all-hashtag.com/library/contents/ajax_generator.php"

@DAXX.on_message(filters.command("hastag"))
async def hastag(bot, message):
    try:
        # Ensure the user provides a keyword
        text = message.text.split(' ', 1)[1]
        data = dict(keyword=text, filter="top")
        
        # Make the POST request
        res = requests.post(url, data)
        
        # Check for successful request
        if res.status_code != 200:
            return await message.reply_text("Failed to retrieve hashtags. Please try again later.")
        
        # Parse the response and extract hashtags
        content = BSP(res.text, 'html.parser').find("div", {"class": "copy-hashtags"})
        
        if content:
            hashtags = content.get_text(strip=True)
        else:
            return await message.reply_text("No hashtags found for this keyword.")
        
    except IndexError:
        return await message.reply_text("Please provide a keyword. Example: `/hastag python`")
    except Exception as e:
        # Catch any other errors and inform the user
        return await message.reply_text(f"An error occurred: {str(e)}")
    
    # Send the result
    await message.reply_text(f"ʜᴇʀᴇ ɪs ʏᴏᴜʀ ʜᴀsᴛᴀɢ :\n<pre>{hashtags}</pre>", quote=True)


mod_name = "Hᴀsʜᴛᴀɢ"
help = """
Yᴏᴜ ᴄᴀɴ ᴜsᴇ ᴛʜɪs ʜᴀsʜᴛᴀɢ ɢᴇɴᴇʀᴀᴛᴏʀ ᴡʜɪᴄʜ ᴡɪʟʟ ɢɪᴠᴇ ʏᴏᴜ ᴛʜᴇ ᴛᴏᴘ 𝟹𝟶 ᴀɴᴅ ᴍᴏʀᴇ ʜᴀsʜᴛᴀɢs ʙᴀsᴇᴅ ᴏғғ ᴏғ ᴏɴᴇ ᴋᴇʏᴡᴏʀᴅ sᴇʟᴇᴄᴛɪᴏɴ.
° /hastag enter word to generate hastag.
°Exᴀᴍᴘʟᴇ:  /hastag python
"""
