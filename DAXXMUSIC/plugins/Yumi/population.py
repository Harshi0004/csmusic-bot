from pyrogram import Client, filters
from pyrogram.types import Message
import requests
from DAXXMUSIC import app

@app.on_message(filters.command("population"))
def country_command_handler(client: Client, message: Message):
    # Ensure a country code is provided
    if len(message.text.split()) < 2:
        return message.reply_text("Please provide a country code. Example: /population IN")

    # Extract the country code from the command
    country_code = message.text.split(maxsplit=1)[1].strip()

    # Call the external API for country information
    api_url = f"https://restcountries.com/v3.1/alpha/{country_code}"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        country_info = response.json()
        if country_info:
            # Extract relevant information from the API response
            country_name = country_info[0].get("name", {}).get("common", "N/A")
            capital = country_info[0].get("capital", ["N/A"])[0]
            population = country_info[0].get("population", "N/A")
            region = country_info[0].get("region", "N/A")
            subregion = country_info[0].get("subregion", "N/A")
            flag = country_info[0].get("flags", {}).get("png", "N/A")
            languages = ", ".join(country_info[0].get("languages", {}).values()) if country_info[0].get("languages") else "N/A"

            # Formulate the response
            response_text = (
                f"<b>Country Information</b>\n\n"
                f"🇨🇭 <b>Name:</b> {country_name}\n"
                f"🏙️ <b>Capital:</b> {capital}\n"
                f"🌍 <b>Region:</b> {region}\n"
                f"🌏 <b>Subregion:</b> {subregion}\n"
                f"💰 <b>Population:</b> {population}\n"
                f"🗣️ <b>Languages:</b> {languages}\n"
                f"🌐 <b>Flag:</b> {flag}"
            )
        else:
            response_text = "Error fetching country information. Please verify the country code."

    except requests.exceptions.HTTPError:
        response_text = "Invalid country code or no data available for the provided code."
    except Exception as err:
        response_text = f"An error occurred while fetching the information. Error: {str(err)}"

    # Send the response to the Telegram chat
    message.reply_text(response_text, parse_mode="HTML")
