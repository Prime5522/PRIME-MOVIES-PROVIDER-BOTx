from pyrogram import Client, filters
import requests
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import OMDB_API_KEY, TARGET_CHANNEL_ID  # info.py থেকে ডাটা ইমপোর্ট করুন

app = Client("my_bot")  # Pyrogram Client তৈরি করুন

@app.on_message(filters.channel & filters.document)
def handle_new_file(client, message):
    file_name = message.document.file_name
    file_id = message.document.file_id
    file = client.get_file(file_id)
    direct_link = f"https://api.telegram.org/file/bot{client.bot_token}/{file.file_path}"

    movie_name = file_name.rsplit(".", 1)[0]

    # OMDb API থেকে মুভির তথ্য পাওয়া
    response = requests.get(f"http://www.omdbapi.com/?t={movie_name}&apikey={OMDB_API_KEY}")
    movie_data = response.json()

    if movie_data.get("Response") == "True":
        title = movie_data.get("Title", "Unknown Title")
        year = movie_data.get("Year", "Unknown Year")
        rating = movie_data.get("imdbRating", "N/A")
        plot = movie_data.get("Plot", "No plot available")
        poster_url = movie_data.get("Poster", "")

        # পোস্টের জন্য টেক্সট তৈরি
        post_text = f"🎬 **{title} ({year})**\n\n⭐️ IMDB Rating: {rating}\n\n📖 Plot: {plot}"

        # ফটো সহ পোস্ট পাঠানো
        client.send_photo(
            chat_id=TARGET_CHANNEL_ID,
            photo=poster_url,
            caption=post_text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Download Now", url=direct_link)]]
            )
        )

# বট চালু করা
app.run()
