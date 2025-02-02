from pyrogram import Client, filters
import requests
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Config থেকে API Key & Channel ID ইমপোর্ট করুন
from config import OMDB_API_KEY, TARGET_CHANNEL_ID

@app.on_message(filters.channel & filters.document)
def handle_new_file(client, message):
    file_name = message.document.file_name
    file_id = message.document.file_id
    file = client.get_file(file_id)
    direct_link = f"https://api.telegram.org/file/bot{client.bot_token}/{file.file_path}"

    movie_name = file_name.rsplit(".", 1)[0]

    response = requests.get(f"http://www.omdbapi.com/?t={movie_name}&apikey={OMDB_API_KEY}")
    movie_data = response.json()

    if movie_data["Response"] == "True":
        title = movie_data["Title"]
        year = movie_data["Year"]
        rating = movie_data["imdbRating"]
        plot = movie_data["Plot"]
        poster_url = movie_data["Poster"]

        post_text = f"🎬 **{title} ({year})**\n\n⭐️ IMDB Rating: {rating}\n\n📖 Plot: {plot}"

        client.send_photo(
            chat_id=TARGET_CHANNEL_ID,
            photo=poster_url,
            caption=post_text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Download Now", url=direct_link)]]
            )
  )
