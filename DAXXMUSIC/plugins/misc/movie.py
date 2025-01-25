import aiohttp
from pyrogram import Client, filters
from DAXXMUSIC import app

TMDB_API_KEY = "23c3b139c6d59ebb608fe6d5b974d888"

# Function to fetch movie info from TMDB API
async def get_movie_info(movie_name):
    tmdb_api_url = f"https://api.themoviedb.org/3/search/movie"
    params = {"api_key": TMDB_API_KEY, "query": movie_name}
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(tmdb_api_url, params=params) as response:
                data = await response.json()

                if response.status != 200:
                    return f"Error: Unable to fetch data from TMDb API. Status Code: {response.status}"

                if not data.get("results"):
                    return "Movie not found or no results returned."

                # Get the first movie from the results
                movie = data["results"][0]

                # Fetch additional details for the movie
                details_url = f"https://api.themoviedb.org/3/movie/{movie['id']}"
                details_params = {"api_key": TMDB_API_KEY}
                async with session.get(details_url, params=details_params) as details_response:
                    details_data = await details_response.json()

                    if details_response.status != 200:
                        return f"Error: Unable to fetch details for the movie. Status Code: {details_response.status}"

                    # Extract relevant information from the movie details
                    title = details_data.get("title", "N/A")
                    release_date = details_data.get("release_date", "N/A")
                    overview = details_data.get("overview", "N/A")
                    vote_average = details_data.get("vote_average", "N/A")
                    revenue = details_data.get("revenue", "N/A")
                    providers = details_data.get("providers", {}).get("results", {}).get("US", {}).get("flatrate", [])
                    providers = ", ".join([provider["provider_name"] for provider in providers]) if providers else "N/A"
                    
                    # Get cast (actors)
                    cast_url = f"https://api.themoviedb.org/3/movie/{movie['id']}/credits"
                    async with session.get(cast_url, params=details_params) as cast_response:
                        cast_data = await cast_response.json()
                        if cast_response.status != 200:
                            return f"Error: Unable to fetch cast details. Status Code: {cast_response.status}"

                        actors = ", ".join([actor["name"] for actor in cast_data.get("cast", [])]) if cast_data.get("cast") else "N/A"

                    # Format the movie details
                    info = (
                        f"**Title**: {title}\n"
                        f"**Release Date**: {release_date}\n"
                        f"**Overview**: {overview}\n"
                        f"**Vote Average**: {vote_average}\n"
                        f"**Actors**: {actors}\n"
                        f"**Total Collection**: {revenue}\n"
                        f"**Available Platforms**: {providers}\n"
                    )
                    return info
    except Exception as e:
        return f"An error occurred while fetching movie information: {str(e)}"

@app.on_message(filters.command("movie"))
async def movie_command(client, message):
    try:
        # Check if the user provided a movie name after the /movie command
        if len(message.command) > 1:
            movie_name = " ".join(message.command[1:])

            # Fetch movie information asynchronously
            movie_info = await get_movie_info(movie_name)

            # Send the movie information as a reply
            await message.reply_text(movie_info)
        else:
            await message.reply_text("Please enter a movie name after the /movie command.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")
