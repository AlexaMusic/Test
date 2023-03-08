from pyrogram import Client, filters
from pyrogram.types import Message
import requests
import os


API_ID = os.environ.get("API_ID", None) 
API_HASH = os.environ.get("API_HASH", None) 
BOT_TOKEN = os.environ.get("BOT_TOKEN", None) 


app = Client(
    "TikTok" ,
    api_id = API_ID,
    api_hash = API_HASH ,
    bot_token = BOT_TOKEN
)

@app.on_message(filters.command(["start"]))
async def start_handler(client, message):
    await message.reply_text("Hi! Send me a TikTok video link and I'll download it for you without a watermark.")


@app.on_message(filters.regex(r"^(https?\:\/\/)?(www\.)?tiktok\.com\/.+"))
async def download_handler(client, message):
    url = message.text
    await message.reply_chat_action("typing")
    response = requests.get(f"https://www.tiktok.com/oembed?url={url}")
    video_url = response.json()["video_url"].replace("https://", "http://")
    await message.reply_video(video_url)


app.run()
