import os
import requests
import openai
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

API_ID = os.environ.get("API_ID", None) 
API_HASH = os.environ.get("API_HASH", None) 
BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
openai.api_key = os.environ.get("OPENAI_API_KEY", None)

bot = Client(
    "AlexaBot" ,
    api_id = API_ID,
    api_hash = API_HASH ,
    bot_token = BOT_TOKEN
)

welcome_message = "Welcome to the group voice chat, {first_name}! Your user ID is {user_id} and your username is @{username}."


@bot.on_message(filters.command("start") & filters.private & ~filters.edited)
async def start(client, m: Message):
    await m.delete()
    alexaai = await m.reply("🤭🤏✌️")
    await asyncio.sleep(1)
    await alexaai.edit("**sᴛᴀʀᴛɪɴɢ ʙᴏᴛ**")
    await asyncio.sleep(1)
    await alexaai.edit("**ɪ ᴀᴍ ᴅᴏɪɴɢ ᴍʏ ʟᴏᴠᴇ 💕**")
    await alexaai.delete()
    await asyncio.sleep(2)
    umm = await m.reply_sticker("CAACAgIAAxkBAAEForNjAykaq_efq4Wd-9KZv-nNxJRn3AACIgMAAm2wQgO8x8PfoXC1eCkE")
    await asyncio.sleep(2)
    await m.reply_photo(
        photo=f"https://telegra.ph/file/1730f54f033ad0d2b91d2.jpg",
        caption=f"""━━━━━━━━━━━━━━━━━━━━━━━━\n\n✪ ᴛʜɪs ɪs ᴀʟᴇxᴀ ᴀɪ ᴀᴅᴠᴀɴᴄᴇᴅ ᴄʜᴀᴛʙᴏᴛ ʙᴀsᴇᴅ ᴏɴ ʙᴀᴄᴋᴇɴᴅ ᴅᴀᴛᴀʙᴀsᴇ\n✪ ᴛʜᴀɴᴋs ᴛᴏ  ᴀʟᴇxᴀ ᴛᴇᴀᴍ 🌼 ..\n\n┏━━━━━━━━━━━━━━━━━┓\n┣★ ᴏᴡɴᴇʀ    : [ᴀsᴀᴅ ᴀʟɪ](https://t.me/Dr_Asad_Ali)\n┣★ ᴜᴘᴅᴀᴛᴇs › : [ᴀʟᴇxᴀ ʜᴇʟᴘ](https://t.me/Alexa_BotUpdates)\n┣★ ʀᴇᴘᴏ › : [ᴀʟᴇxᴀ ᴀɪ ʀᴇᴘᴏ](https://github.com/TheTeamAlexa/AlexaAiMachineBot)\n┗━━━━━━━━━━━━━━━━━┛\n\n💞 ɪғ ʏᴏᴜ ʜᴀᴠᴇ ᴀɴʏ ǫᴜᴇsᴛɪᴏɴs ᴛʜᴇɴ\nᴅᴍ ᴛᴏ ᴍʏ [ᴏᴡɴᴇʀ](https://t.me/Jankari_Ki_Duniya) ᴍᴀᴋᴇ sᴜʀᴇ ᴛᴏ sᴛᴀʀ ᴏᴜʀ ᴘʀᴏᴊᴇᴄᴛ ...\n\n━━━━━━━━━━━━━━━━━━━━━━━━
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "+ ᴀᴅᴅ ᴍᴇ +",
                        url=f"https://t.me/ROCKS_KITTY_BOT?startgroup=true",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🌼 ᴀʟᴇxᴀ ᴄʜᴀᴛ︎", url=f"https://t.me/Alexa_Help"
                    ),
                    InlineKeyboardButton(
                        "ʀᴏᴄᴋs 🌷", url=f"https://t.me/Shayri_Music_Lovers"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "💞 sᴛᴀғғ 💘", url="https://t.me/ROCKS_OFFICIAL/119"
                    )
                ],
            ]
        ),
    )
  
WELCOME_MESSAGE = """
Hi there! I'm a language model trained by OpenAI. You can ask me anything and I'll try my best to respond. To get started, type /generate to generate some text.
"""

def generate_text(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response.choices[0].text

@bot.on_message(filters.command("start"))
def start_command_handler(client, message):
    client.send_message(
        chat_id=message.chat.id,
        text=WELCOME_MESSAGE,
        reply_to_message_id=message.message_id,
    )

@bot.on_message(filters.command("generate"))
def generate_command_handler(client, message):
    prompt = "Ask me a question and I'll generate an answer!"
    text = generate_text(prompt)
    client.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_to_message_id=message.message_id,
    )
            
bot.run()
