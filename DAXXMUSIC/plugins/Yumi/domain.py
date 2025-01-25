from pyrogram import Client, filters
import whois
from DAXXMUSIC import app

def get_domain_hosting_info(domain_name):
    try:
        domain_info = whois.whois(domain_name)
        return domain_info
    except whois.parser.PywhoisError as e:
        print(f"Error: {e}")
        return None

@app.on_message(filters.command("domain"))
async def get_domain_info(client, message):
    if len(message.command) > 1:
        domain_name = message.command[1].strip()  # Get domain name without extra spaces

        if not domain_name:
            await message.reply("Please provide a valid domain name after the /domain command.")
            return

        domain_info = get_domain_hosting_info(domain_name)

        if domain_info:
            # Build the response with available domain info
            response = f"🔍 **Domain Information for {domain_name}:**\n\n"
            response += f"📅 **Registrar:** {domain_info.registrar if domain_info.registrar else 'Not available'}\n"
            response += f"📆 **Creation Date:** {domain_info.creation_date if domain_info.creation_date else 'Not available'}\n"
            response += f"⏳ **Expiration Date:** {domain_info.expiration_date if domain_info.expiration_date else 'Not available'}\n"
            response += f"🌐 **Name Servers:** {', '.join(domain_info.name_servers) if domain_info.name_servers else 'Not available'}\n"
            response += f"📍 **Registrant:** {domain_info.registrant if domain_info.registrant else 'Not available'}\n"
            response += f"🔄 **Updated Date:** {domain_info.updated_date if domain_info.updated_date else 'Not available'}\n"
        else:
            response = "❌ Failed to retrieve domain hosting information. Please check the domain name or try again later."

        await message.reply(response)
    else:
        await message.reply("❗ Please provide a domain name after the /domain command. Example: `/domain example.com`")
