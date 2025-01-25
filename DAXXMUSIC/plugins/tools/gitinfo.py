import asyncio, os, time, aiohttp
from pyrogram import filters
from daxxhub import daxxhub as papadaxx
from DAXXMUSIC import app
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Handle daxxhub command
@app.on_message(filters.command("daxxhub"))
async def daxxhub(_, message):
    text = message.text[len("/daxxhub") :].strip()
    if not text:
        await message.reply_text("Please provide a valid text for the image!")
        return

    # Create the image and send it
    file_name = f"daxxhub_{message.from_user.id}.png"
    try:
        papadaxx(text).save(file_name)
        await message.reply_photo(file_name)
    except Exception as e:
        await message.reply_text(f"An error occurred while generating the image: {str(e)}")
    finally:
        if os.path.exists(file_name):
            os.remove(file_name)  # Cleanup

# Handle github command
@app.on_message(filters.command(["github", "git"]))
async def github(_, message):
    if len(message.command) != 2:
        await message.reply_text("Usage: /git <GitHub Username>")
        return

    username = message.text.split(None, 1)[1]
    URL = f'https://api.github.com/users/{username}'

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(URL) as request:
                if request.status == 404:
                    return await message.reply_text(f"User '{username}' not found on GitHub!")
                
                result = await request.json()

                url = result.get('html_url')
                name = result.get('name', 'N/A')
                company = result.get('company', 'N/A')
                bio = result.get('bio', 'N/A')
                created_at = result.get('created_at', 'N/A')
                avatar_url = result.get('avatar_url', '')
                blog = result.get('blog', 'N/A')
                location = result.get('location', 'N/A')
                repositories = result.get('public_repos', 0)
                followers = result.get('followers', 0)
                following = result.get('following', 0)

                caption = f"""GitHub Info for {name}

Username: {username}
Bio: {bio}
Link: [Here]({url})
Company: {company}
Created On: {created_at}
Repositories: {repositories}
Blog: {blog}
Location: {location}
Followers: {followers}
Following: {following}"""

                # Create the inline keyboard with a close button
                close_button = InlineKeyboardButton("Close", callback_data="close")
                inline_keyboard = InlineKeyboardMarkup([[close_button]])

                # Send the message with the inline keyboard
                if avatar_url:
                    await message.reply_photo(photo=avatar_url, caption=caption, reply_markup=inline_keyboard)
                else:
                    await message.reply_text(caption, reply_markup=inline_keyboard)

        except Exception as e:
            await message.reply_text(f"An error occurred while fetching GitHub info: {str(e)}")

# Handle callback query for closing the message
@app.on_callback_query(filters.regex("close"))
async def close_button(_, cq):
    await cq.message.delete()
    await cq.answer()
