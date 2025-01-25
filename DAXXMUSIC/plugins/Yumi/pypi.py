from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import requests
from DAXXMUSIC import app

def get_pypi_info(package_name):
    try:
        api_url = f"https://pypi.org/pypi/{package_name}/json"
        
        # Sending a request to the PyPI API
        response = requests.get(api_url)
        
        # Handling non-existent packages
        if response.status_code != 200:
            return None
        
        # Extracting information from the API response
        pypi_info = response.json()
        return pypi_info
    
    except Exception as e:
        print(f"Error fetching PyPI information: {e}")
        return None

@app.on_message(filters.command("pypi", prefixes="/"))
def pypi_info_command(client, message):
    try:
        # Extracting the package name
        if len(message.command) < 2:
            return client.send_message(message.chat.id, "Please provide a package name after the /pypi command. Example: /pypi requests")
        
        package_name = message.command[1]
        
        # Getting information from PyPI
        pypi_info = get_pypi_info(package_name)
        
        if pypi_info:
            # Creating a message with PyPI information
            info_message = (
                f"🔹 <b>Package Name:</b> {pypi_info['info']['name']}\n\n"
                f"🔹 <b>Latest Version:</b> {pypi_info['info']['version']}\n\n"
                f"🔹 <b>Description:</b> {pypi_info['info']['summary']}\n\n"
                f"🔹 <b>Project URL:</b> {pypi_info['info']['project_urls']['Homepage']}"
            )
            
            # Sending the PyPI information back to the user
            client.send_message(message.chat.id, info_message, parse_mode="HTML")
        
        else:
            # Handling the case where the package doesn't exist
            client.send_message(message.chat.id, f"Sorry, no information found for the package <code>{package_name}</code>. Please ensure the package name is correct.", parse_mode="HTML")
    
    except IndexError:
        client.send_message(message.chat.id, "Please provide a package name after the /pypi command. Example: /pypi requests")
    
    except Exception as e:
        client.send_message(message.chat.id, f"An error occurred: {str(e)}")
