from pyrogram import Client, filters
from TikTokApi import TikTokApi


API_ID = os.environ.get("API_ID", None) 
API_HASH = os.environ.get("API_HASH", None) 
BOT_TOKEN = os.environ.get("BOT_TOKEN", None) 


app = Client(
    "TikTok" ,
    api_id = API_ID,
    api_hash = API_HASH ,
    bot_token = BOT_TOKEN
)

api = TikTokApi.get_instance()

@app.on_message(filters.command("download") & filters.private)
async def download_tiktok(client, message):
    url = message.text.split()[1]
    video_bytes = api.get_video_by_url(url, no_watermark=True)
    await client.send_video(
        chat_id=message.chat.id,
        video=video_bytes,
        caption="Here's your TikTok video!",
    )

app.run()
