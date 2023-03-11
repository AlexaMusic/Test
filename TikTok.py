import os
import requests
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

API_ID = os.environ.get("API_ID", None) 
API_HASH = os.environ.get("API_HASH", None) 
BOT_TOKEN = os.environ.get("BOT_TOKEN", None)

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
  
@bot.on_message(filters.text)
async def on_message(client, message):
    chat = await client.get_chat(message.chat.id)
    if chat.type == "voice":
        for member in message.new_chat_members:
            if member.is_self:
                continue
            chat_type = "channel" if chat.type == "channel" else "group"
            chat_info = f"{chat.title} ({chat.id})"
            first_name = member.first_name
            user_id = member.id
            username = member.username
            notification_text = notification_message.format(chat_type=chat_type, chat_info=chat_info, first_name=first_name, user_id=user_id, username=username)
            await client.send_message(chat.id, notification_text)
            chat_members = await client.get_chat_members(chat.id)
            user_ids = [member.user.id for member in chat_members]
            if user_id not in user_ids:
                welcome_text = welcome_message.format(first_name=first_name, user_id=user_id, username=username)
                await client.send_message(user_id, welcome_text)


            
bot.run()
