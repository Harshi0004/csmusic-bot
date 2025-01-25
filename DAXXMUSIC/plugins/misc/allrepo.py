import aiohttp
from pyrogram import Client, filters
from DAXXMUSIC import app

# Function to chunk the repository info into smaller parts
def chunk_string(text, chunk_size):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

@app.on_message(filters.command("allrepo"))
async def all_repo_command(client, message):
    try:
        # Check if there is a GitHub username after the /allrepo command
        if len(message.command) > 1:
            github_username = message.command[1]

            # Fetch information about all repositories of the GitHub user
            repo_info = await get_all_repository_info(github_username)

            # Split repository info into smaller chunks
            chunked_repo_info = chunk_string(repo_info, 4000)  # Split into chunks of 4000 characters

            # Send the repository information in chunks as separate messages
            for chunk in chunked_repo_info:
                await message.reply_text(chunk)
        else:
            await message.reply_text("Please enter a GitHub username after the /allrepo command.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")


async def get_all_repository_info(github_username):
    # Set up the GitHub API URL for user repositories
    github_api_url = f"https://api.github.com/users/{github_username}/repos"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(github_api_url) as response:
                # Check if we hit the rate limit
                if response.status == 403:
                    return "Rate limit exceeded. Please try again later."

                if response.status != 200:
                    return f"Failed to fetch repositories. HTTP Status: {response.status}"

                # Parse the JSON response
                data = await response.json()

                if not data:
                    return "No repositories found for this user."

                # Extract relevant information from the response
                repo_info = "\n\n".join([
                    f"Repository: {repo['full_name']}\n"
                    f"Description: {repo['description']}\n"
                    f"Stars: {repo['stargazers_count']}\n"
                    f"Forks: {repo['forks_count']}\n"
                    f"URL: {repo['html_url']}"
                    for repo in data
                ])

                return repo_info
    except Exception as e:
        return f"An error occurred while fetching repository information: {str(e)}"
