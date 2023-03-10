import os
import re
import time
import psutil
import asyncio
import traceback
from data import Data
from datetime import datetime
from pyrogram import Client, filters, __version__ as pyrover
from pyrogram.types import *
from pymongo import MongoClient
import requests
import random
from pyrogram.errors import (
    PeerIdInvalid,
    ChatWriteForbidden
)
from pyrogram.types import Dialog, Chat, Message
from pyrogram.errors import UserAlreadyParticipant
from typing import Union
from pyrogram.errors import FloodWait
from filters import command
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden
from Database import (add_gban_user,
                                       get_gbans_count,
                                       add_served_chat,
                                       get_served_users,
                                       add_served_user,
                                       get_served_chats,
                                       get_banned_users,
                                       get_served_chats,
                                       is_gbanned_user,
                                       remove_gban_user)

API_ID = os.environ.get("API_ID", None) 
API_HASH = os.environ.get("API_HASH", None) 
BOT_TOKEN = os.environ.get("BOT_TOKEN", None) 
MONGO_URL = os.environ.get("MONGO_URL", None)
MUST_JOIN = os.environ.get("MUST_JOIN", None)

OWNER = 6174058850
chat_watcher_group = 10
BANNED_USERS = filters.user()


bot = Client(
    "AlexaBot" ,
    api_id = API_ID,
    api_hash = API_HASH ,
    bot_token = BOT_TOKEN
)


async def is_admins(chat_id: int):
    return [
        member.user.id
        async for member in bot.iter_chat_members(
            chat_id, filter="administrators"
        )
    ]

async def bot_sys_stats():
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    stats = f"""
ᴄᴘᴜ: {cpu}%
ʀᴀᴍ: {mem}%
ᴅɪsᴋ: {disk}%
ᴊᴏɪɴ: @Alexa.Help"""
    return stats


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix_list[i]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time

async def log_message(chat_id: int, message: str):
    await bot.send_message(chat_id=chat_id, text=message)

slang_words = ['fuck', 'land', 'mc', 'bc', 'chut', 'madar)', 'bak', 'bbiab', 'bbl', 'bbs', 'brb', 'btw', 'cul8r', 'f2f', 'fwiw', 'fyi', 'g2g', 'gtg', 'ic', 'idk', 'ikr', 'imho', 'imo', 'irl', 'jk', 'jmo', 'k', 'l8r', 'lmao', 'lmk', 'lol', 'nbd', 'nvm', 'omg', 'rofl', 'stfu', 'thx', 'tmi', 'ttyl', 'wtf', 'wyd', 'yolo', 'ywy', 'zzz']

@bot.on_message(filters.new_chat_members)
async def on_new_chat_members(client: Client, message: Message):
    if client.get_me().id in [user.id for user in message.new_chat_members]:
        added_by = message.from_user.first_name if message.from_user else "unknown user"
        matlabi_jhanto = message.chat.title
        chat_id = message.chat.id
        if message.chat.username:
            chatusername = f"@{message.chat.username}"
        else:
            chatusername = "ᴩʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ"
        log_text = f"Bot added to new group '{matlabi_jhanto}' ({chat_id}) by {added_by} Chat Usernaem {chatusername}"
        await log_message(LOG_GROUP_ID, log_text)

@bot.on_message(filters.command("start") & filters.private & ~filters.edited)
async def start(client, m: Message):
    await add_served_user(m.from_user.id)
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
    
    
@bot.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channel(bot: Client, msg: Message):
    if not MUST_JOIN:  # Not compulsory
        return
    try:
        try:
            await bot.get_chat_member(MUST_JOIN, msg.from_user.id)
        except UserNotParticipant:
            if MUST_JOIN.isalpha():
                link = "https://t.me/" + MUST_JOIN
            else:
                chat_info = await bot.get_chat(MUST_JOIN)
                link = chat_info.invite_link
            try:
                await msg.reply(
                    f"ʏᴏᴜ ᴍᴜsᴛ ᴊᴏɪɴ [ᴛʜɪs ᴄʜᴀɴɴᴇʟ]({link}) ᴛᴏ ᴜsᴇ ᴍᴇ. ᴀꜰᴛᴇʀ ᴊᴏɪɴɪɴɢ ᴛʀʏ ᴀɢᴀɪɴ!",
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("✨ ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ ✨", url=link)]]
                    ),
                )
                await msg.stop_propagation()
            except ChatWriteForbidden:
                pass
    except ChatAdminRequired:
        print(f"ɪ'ᴍ ɴᴏᴛ ᴀᴅᴍɪɴ ɪɴ MUST_JOIN ᴄʜᴀᴛ : {MUST_JOIN} !")
    
@bot.on_message(filters.command("repo") & filters.private & ~filters.edited)
async def repo(client, message):
    await add_served_user(message.from_user.id)
    await message.reply_photo(
        photo=f"https://telegra.ph/file/2fabd1c33e888e0533891.jpg",
        caption=f"""━━━━━━━━━━━━━━━━━━━━━━━━
💥 A ᴘᴏᴡᴇʀғᴜʟ ᴀɪ ʙᴏᴛ
ᴏғ ♻️ ᴅʀ ᴀsᴀᴅ ᴀʟɪ 🔥
━━━━━━━━━━━━━━━━━
ᴅᴀᴛᴀʙᴀsᴇ ʙᴀᴄᴋᴇɴᴅ ʙᴏᴛ ғᴏʀ ᴛɢ...
┏━━━━━━━━━━━━━━━━━┓
┣★ ᴄʀᴇᴀᴛᴇʀ [ᴀsᴀᴅ ᴀʟɪ](https://t.me/Dr_Asad_Ali)
┣★ ʜᴇᴀʀᴛ ᴜs  [ʜᴇᴀʀᴛ ❤️](https://t.me/Give_Me_Heart)
┣★ ʙᴏᴛ ᴜᴏᴅᴀᴛᴇs [ᴏᴜʀ ᴏᴛʜᴇʀ ʙᴏᴛs](https://t.me/Alexa_BotUpdates)
┣★ ᴀʟᴇxᴀ ғᴇᴅ [ғᴇᴅ ʟᴏɢs](https://t.me/AlexaFed_Logs)
┣★ sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ : [ᴄʟɪᴄᴋ ʜᴇʀᴇ](https://github.com/TheTeamAlexa/AlexaAiMachineBot)
┣★ ɴᴇᴛᴡᴏʀᴋ [ʀᴏᴄᴋs](https://t.me/Shayri_Music_Lovers)
┗━━━━━━━━━━━━━━━━━┛
💞 
IF HAVE ANY QUESTION THEN CONTACT » TO » MY » [OWNER] @Jankari_Ki_Duniya""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🌼 ᴀʟᴇxᴀ ᴄʜᴀᴛ 💮", url=f"https://t.me/Alexa_Help")]]
        ),
    )    
@bot.on_message(
    filters.command("chatbot off", prefixes=["/", ".", "?", "-"])
    & ~filters.private)
async def chatbotofd(client, message):
    alexadb = MongoClient(MONGO_URL)    
    alexa = alexadb["AlexaDb"]["Alexa"]     
    if message.from_user:
        user = message.from_user.id
        chat_id = message.chat.id
        if user not in (
           await is_admins(chat_id)
        ):
           return await message.reply_text(
                "You are not admin"
            )
    is_alexa = alexa.find_one({"chat_id": message.chat.id})
    if not is_alexa:
        alexa.insert_one({"chat_id": message.chat.id})
        await message.reply_text(f"ᴄʜᴀᴛʙɪᴛ ɪs ᴅɪsᴀʙʟᴇᴅ ʙʏ {message.from_user.mention()} ғᴏʀ ᴜsᴇʀs ɪɴ {message.chat.title}")
    if is_alexa:
        await message.reply_text(f"ᴄʜᴀᴛʙɪᴛ ɪs ᴀʟʀᴇᴀᴅʏ ᴅɪsᴀʙʟᴇᴅ")

@bot.on_message(command("stats") & filters.user(OWNER) & ~filters.edited)
async def stats(client, m: Message):
    await m.delete()
    alexaai = await m.reply("**ᴡᴀɪᴛ**️")
    await asyncio.sleep(1)
    await alexaai.edit("**ɪ ᴀᴍ ᴄᴏʟʟᴇᴄᴛɪɴɢ sᴛᴀᴛᴜs**")
    await asyncio.sleep(1)
    await alexaai.delete()    
    copypast_lawdey = len(await get_served_users())
    matlabi_jhanto = len(await get_served_chats())
    matlabi_chudo = await get_gbans_count()
    tgm = f"""
➥ 🌹 ➛ **ᴛᴏᴛᴀʟ ᴜsᴇʀs** : {copypast_lawdey}
➥ 🌹 ➛ **ᴛᴏᴛᴀʟ ɢʀᴏᴜᴘs** : {matlabi_jhanto}
➥ 🌹 ➛ **ᴛᴏᴛᴀʟ ʙᴀɴ ᴜsᴇʀs** : {matlabi_chudo}
➥ 🌹 ➛ **ᴘʏʀᴏ ᴠᴇʀsɪᴏɴ** : {pyrover}

**──────────────**"""
    await m.reply(tgm, disable_web_page_preview=True)


@bot.on_message(
    filters.command("chatbot on", prefixes=["/", ".", "?", "-"])
    & ~filters.private)
async def chatboton(client, message):
    alexadb = MongoClient(MONGO_URL)    
    alexa = alexadb["AlexaDb"]["Alexa"]     
    if message.from_user:
        user = message.from_user.id
        chat_id = message.chat.id
        if user not in (
            await is_admins(chat_id)
        ):
            return await message.reply_text(
                "You are not admin"
            )
    is_alexa = alexa.find_one({"chat_id": message.chat.id})
    if not is_alexa:           
        await message.reply_text(f"ᴄʜᴀᴛʙɪᴛ ɪs ᴀʟʀᴇᴀᴅʏ ᴇɴᴀʙʟᴇᴅ")
    if is_alexa:
        alexa.delete_one({"chat_id": message.chat.id})
        await message.reply_text(f"ᴄʜᴀᴛʙɪᴛ ɪs ᴇɴᴀʙʟᴇᴅ ʙʏ {message.from_user.mention()} ғᴏʀ ᴜsᴇʀs ɪɴ {message.chat.title}")


@bot.on_message(
    filters.command("chatbot", prefixes=["/", ".", "?", "-"])
    & ~filters.private)
async def chatbot(client, message):
    await add_served_user(message.from_user.id)
    await message.reply_text(f"**ᴜsᴇᴀɢᴇ:**\n/chatbot [on|off] only group")



@bot.on_message(filters.command("info"))
def info(_, message):
    if message.text == "/info":
        user = message.from_user.id
    if message.reply_to_message:
        user = message.reply_to_message.from_user.id
    if user == OWNER:
        status = "**ᴛʜɪs ᴘᴇʀsᴏɴ ɪs ᴍʏ ᴏᴡɴᴇʀ ᴍʏ ʟᴏʙ ᴍᴏɪ ᴇᴠᴇʀʏᴛʜɪɴɢ**"
    else:
        status = "member"

    pfp_count = bot.get_profile_photos_count(user)

    if not pfp_count == 0:
        pfp = bot.get_profile_photos(user, limit=1)
        pfp_ = pfp[0]['thumbs'][0]['file_id']

    foo = bot.get_users(user)
    data = f"""**ғɪʀsᴛ ɴᴀᴍᴇ** : {foo.first_name}
**ʟᴀsᴛ ɴᴀᴍᴇ**: {foo.last_name}
**ᴛᴇʟᴇɢʀᴀᴍ Id**: {foo.id}
**ᴄʜᴀᴛ ʟɪɴᴋ**: {foo.mention(foo.first_name)}
**ɪs ʙᴏᴛ**: {foo.is_bot}
**sᴛᴀᴛᴜs**: {status}
"""

    if pfp_count != 0:
        message.reply_photo(pfp_, caption=data)

    else:
        message.reply_text(data)
                                                                                                                                                                                                                  

@bot.on_message(filters.command("ping"))
async def ping(_, message):
    start = datetime.now()
    response = await message.reply_photo(
        photo="https://telegra.ph/file/ffd8950793c85d44c0f44.jpg",
        caption="🌸 ᴘɪɴɢ...",
    )
    uptime = await bot_sys_stats()
    end = datetime.now()
    resp = (end - start).microseconds / 1000
    await response.edit_text(
        f"**💐 ᴘᴏɴɢ**\n`⚡{resp} ᴍs`\n\n**ᴀʟᴇxᴀ ᴀɪ sʏsᴛᴇᴍ\n\n**ᴊᴏɪɴ** @Alexa_Help"
    )


@bot.on_message(group=chat_watcher_group)
async def chat_watcher_func(app: Client, message):
    chat_id = message.chat.id
    await add_served_chat(chat_id)


@bot.on_message(command("bcast_pin") & filters.user(OWNER))
async def broadcast_message_pin(app: Client, message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        pin = 0
        chats = []
        groups = await get_served_chats()
        for chat in groups:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await app.forward_messages(i, y, x)
                try:
                    await m.pin(disable_notification=False)
                    pin += 1
                except Exception:
                    pass
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(Data.BCAST_PIN.format(sent, pin))
        return
    if len(message.command) < 2:
        await message.reply_text(Data.BCAST_USG)
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    pin = 0
    chats = []
    groups = await get_served_chats()
    for chat in groups:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await app.send_message(i, text=text)
            try:
                await m.pin(disable_notification=False)
                pin += 1
            except Exception:
                pass
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(Data.BCAST_PIN.format(sent, pin))


@bot.on_message(command("broadcast") & filters.user(OWNER) & ~filters.edited)
async def broadcast_message(app: Client, message):
    if len(message.command) < 2:
        return await message.reply_text(Data.BCAST_USG)
    sleep_time = 0.1
    text = message.text.split(None, 1)[1]
    sent = 0
    groups = await get_served_chats()
    chats = [int(chat["chat_id"]) for chat in groups]
    m = await message.reply_text(
        f"**🤦‍♂️ ʙʀᴏᴀᴅᴄᴀsᴛ ɪɴ 🤭 ᴘʀᴏɢʀᴇss, 🌷 ᴡɪʟʟ ᴛᴀᴋᴇ ✌️** {len(chats) * sleep_time} **sᴇᴄᴏɴᴅs 💞**."
    )
    for i in chats:
        try:
            await app.send_message(i, text=text)
            await asyncio.sleep(sleep_time)
            sent += 1
        except FloodWait as e:
            await asyncio.sleep(int(e.x))
        except Exception:
            pass
    await m.edit(Data.BCAST_DN.format(sent))
 
@bot.on_message(command("gban") & filters.user(OWNER) & ~filters.edited)
async def gbanuser(app: Client, message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(Data.GBAN_0)
        user = message.text.split(None, 1)[1]
        user = await app.get_users(user)
        user_id = user.id
        mention = user.mention
    else:
        user_id = message.reply_to_message.from_user.id
        mention = message.reply_to_message.from_user.mention
    if user_id == message.from_user.id:
        return await message.reply_text(Data.GBAN_1)
    elif user_id in OWNER:
        return await message.reply_text(Data.GBAN_3)
    is_gbanned = await is_gbanned_user(user_id)
    if is_gbanned:
        return await message.reply_text(Data.GBAN_4.format(mention))
    if user_id not in BANNED_USERS:
        BANNED_USERS.add(user_id)
    served_chats = []
    chats = await get_served_chats()
    for chat in chats:
        served_chats.append(int(chat["chat_id"]))
    time_expected = len(served_chats)
    time_expected = get_readable_time(time_expected)
    mystic = await message.reply_text(
        Data.GBAN_5.format(mention, time_expected, user.id)
    )
    number_of_chats = 0
    for chat_id in served_chats:
        try:
            await app.ban_chat_member(chat_id, user_id)
            number_of_chats += 1
        except FloodWait as e:
            await asyncio.sleep(int(e.x))
        except Exception:
            pass
    await add_gban_user(user_id)
    await message.reply_text(
        Data.GBAN_6.format(mention, number_of_chats)
    )
    await mystic.delete()
    
@bot.on_message(command("ungban") & filters.user(OWNER) & ~filters.edited)
async def ungban_user(app: Client, message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(Data.GBAN_0)
        user = message.text.split(None, 1)[1]
        user = await app.get_users(user)
        user_id = user.id
        mention = user.mention
    else:
        user_id = message.reply_to_message.from_user.id
        mention = message.reply_to_message.from_user.mention
    is_gbanned = await is_gbanned_user(user_id)
    if not is_gbanned:
        return await message.reply_text(Data.GBAN_8.format(mention))
    if user_id in BANNED_USERS:
        BANNED_USERS.remove(user_id)
    served_chats = []
    chats = await get_served_chats()
    for chat in chats:
        served_chats.append(int(chat["chat_id"]))
    time_expected = len(served_chats)
    time_expected = get_readable_time(time_expected)
    mystic = await message.reply_text(
        Data.GBAN_9.format(mention, time_expected)
    )
    number_of_chats = 0
    for chat_id in served_chats:
        try:
            await app.unban_chat_member(chat_id, user_id)
            number_of_chats += 1
        except FloodWait as e:
            await asyncio.sleep(int(e.x))
        except Exception:
            pass
    await remove_gban_user(user_id)
    await message.reply_text(
        Data.GBAN_10.format(mention, number_of_chats)
    )
    await mystic.delete()    
                                                
@bot.on_message(command("gban_list") & filters.user(OWNER) & ~filters.edited)
async def gbanned_list(app: Client, message):
    counts = await get_gbans_count()
    if counts == 0:
        return await message.reply_text(Data.GBAN_7)
    mystic = await message.reply_text(Data.GBAN_8)
    msg = "ɢʙᴀɴɴᴇᴅ ᴜsᴇʀ:\n\n"
    count = 0
    users = await get_banned_users()
    for user_id in users:
        count += 1
        try:
            user = await app.get_users(user_id)
            user = (
                user.first_name if not user.mention else user.mention
            )
            msg += f"{count}➤ {user}\n"
        except Exception:
            msg += f"{count}➤ [Unfetched User]{user_id}\n"
            continue
    if count == 0:
        return await mystic.edit_text(Data.GBAN_7)
    else:
        return await mystic.edit_text(msg)

@bot.on_message(
 (
        filters.text
        | filters.sticker
    )
    & ~filters.private
    & ~filters.bot,
)
async def alexaai(client: Client, message: Message):

   chatdb = MongoClient(MONGO_URL)
   chatai = chatdb["Word"]["WordDb"]   

   if not message.reply_to_message:
       alexadb = MongoClient(MONGO_URL)
       alexa = alexadb["AlexaDb"]["Alexa"] 
       is_alexa = alexa.find_one({"chat_id": message.chat.id})
       if not is_alexa:
           await bot.send_chat_action(message.chat.id, "typing")
           K = []  
           is_chat = chatai.find({"word": message.text})  
           k = chatai.find_one({"word": message.text})      
           if k:               
               for x in is_chat:
                   K.append(x['text'])          
               hey = random.choice(K)
               is_text = chatai.find_one({"text": hey})
               Yo = is_text['check']
               if Yo == "sticker":
                   await message.reply_sticker(f"{hey}")
               if not Yo == "sticker":
                   await message.reply_text(f"{hey}")
   
   if message.reply_to_message:  
       alexadb = MongoClient(MONGO_URL)
       alexa = alexadb["AlexaDb"]["Alexa"] 
       is_alexa = alexa.find_one({"chat_id": message.chat.id})    
       getme = await bot.get_me()
       bot_id = getme.id                             
       if message.reply_to_message.from_user.id == bot_id: 
           if not is_alexa:                   
               await bot.send_chat_action(message.chat.id, "typing")
               K = []  
               is_chat = chatai.find({"word": message.text})
               k = chatai.find_one({"word": message.text})      
               if k:       
                   for x in is_chat:
                       K.append(x['text'])
                   hey = random.choice(K)
                   is_text = chatai.find_one({"text": hey})
                   Yo = is_text['check']
                   if Yo == "sticker":
                       await message.reply_sticker(f"{hey}")
                   if not Yo == "sticker":
                       await message.reply_text(f"{hey}")
       if not message.reply_to_message.from_user.id == bot_id:          
           if message.sticker:
               is_chat = chatai.find_one({"word": message.reply_to_message.text, "id": message.sticker.file_unique_id})
               if not is_chat:
                   chatai.insert_one({"word": message.reply_to_message.text, "text": message.sticker.file_id, "check": "sticker", "id": message.sticker.file_unique_id})
           if message.text:                 
               is_chat = chatai.find_one({"word": message.reply_to_message.text, "text": message.text})                 
               if not is_chat:
                   chatai.insert_one({"word": message.reply_to_message.text, "text": message.text, "check": "none"})    
              

@bot.on_message(
 (
        filters.sticker
        | filters.text
    )
    & ~filters.private
    & ~filters.bot,
)
async def alexastickerai(client: Client, message: Message):

   chatdb = MongoClient(MONGO_URL)
   chatai = chatdb["Word"]["WordDb"]   

   if not message.reply_to_message:
       alexadb = MongoClient(MONGO_URL)
       alexa = alexadb["AlexaDb"]["Alexa"] 
       is_alexa = alexa.find_one({"chat_id": message.chat.id})
       if not is_alexa:
           await bot.send_chat_action(message.chat.id, "typing")
           K = []  
           is_chat = chatai.find({"word": message.sticker.file_unique_id})      
           k = chatai.find_one({"word": message.text})      
           if k:           
               for x in is_chat:
                   K.append(x['text'])
               hey = random.choice(K)
               is_text = chatai.find_one({"text": hey})
               Yo = is_text['check']
               if Yo == "text":
                   await message.reply_text(f"{hey}")
               if not Yo == "text":
                   await message.reply_sticker(f"{hey}")
   
   if message.reply_to_message:
       alexadb = MongoClient(MONGO_URL)
       alexa = alexadb["AlexaDb"]["Alexa"] 
       is_alexa = alexa.find_one({"chat_id": message.chat.id})
       getme = await bot.get_me()
       bot_id = getme.id
       if message.reply_to_message.from_user.id == bot_id: 
           if not is_alexa:                    
               await bot.send_chat_action(message.chat.id, "typing")
               K = []  
               is_chat = chatai.find({"word": message.text})
               k = chatai.find_one({"word": message.text})      
               if k:           
                   for x in is_chat:
                       K.append(x['text'])
                   hey = random.choice(K)
                   is_text = chatai.find_one({"text": hey})
                   Yo = is_text['check']
                   if Yo == "text":
                       await message.reply_text(f"{hey}")
                   if not Yo == "text":
                       await message.reply_sticker(f"{hey}")
       if not message.reply_to_message.from_user.id == bot_id:          
           if message.text:
               is_chat = chatai.find_one({"word": message.reply_to_message.sticker.file_unique_id, "text": message.text})
               if not is_chat:
                   toggle.insert_one({"word": message.reply_to_message.sticker.file_unique_id, "text": message.text, "check": "text"})
           if message.sticker:                 
               is_chat = chatai.find_one({"word": message.reply_to_message.sticker.file_unique_id, "text": message.sticker.file_id})                 
               if not is_chat:
                   chatai.insert_one({"word": message.reply_to_message.sticker.file_unique_id, "text": message.sticker.file_id, "check": "none"})    
               


@bot.on_message(
    (
        filters.text
        | filters.sticker
    )
    & filters.private
    & ~filters.bot,
)
async def alexaprivate(client: Client, message: Message):

   chatdb = MongoClient(MONGO_URL)
   chatai = chatdb["Word"]["WordDb"]
   if not message.reply_to_message: 
       await bot.send_chat_action(message.chat.id, "typing")
       K = []  
       is_chat = chatai.find({"word": message.text})                 
       for x in is_chat:
           K.append(x['text'])
       hey = random.choice(K)
       is_text = chatai.find_one({"text": hey})
       Yo = is_text['check']
       if Yo == "sticker":
           await message.reply_sticker(f"{hey}")
       if not Yo == "sticker":
           await message.reply_text(f"{hey}")
   if message.reply_to_message:            
       getme = await bot.get_me()
       bot_id = getme.id       
       if message.reply_to_message.from_user.id == bot_id:                    
           await bot.send_chat_action(message.chat.id, "typing")
           K = []  
           is_chat = chatai.find({"word": message.text})                 
           for x in is_chat:
               K.append(x['text'])
           hey = random.choice(K)
           is_text = chatai.find_one({"text": hey})
           Yo = is_text['check']
           if Yo == "sticker":
               await message.reply_sticker(f"{hey}")
           if not Yo == "sticker":
               await message.reply_text(f"{hey}")


@bot.on_message(
 (
        filters.sticker
        | filters.text
    )
    & filters.private
    & ~filters.bot,
)
async def alexaprivatesticker(client: Client, message: Message):

   chatdb = MongoClient(MONGO_URL)
   chatai = chatdb["Word"]["WordDb"] 
   if not message.reply_to_message:
       await bot.send_chat_action(message.chat.id, "typing")
       K = []  
       is_chat = chatai.find({"word": message.sticker.file_unique_id})                 
       for x in is_chat:
           K.append(x['text'])
       hey = random.choice(K)
       is_text = chatai.find_one({"text": hey})
       Yo = is_text['check']
       if Yo == "text":
           await message.reply_text(f"{hey}")
       if not Yo == "text":
           await message.reply_sticker(f"{hey}")
   if message.reply_to_message:            
       getme = await bot.get_me()
       bot_id = getme.id       
       if message.reply_to_message.from_user.id == bot_id:                    
           await bot.send_chat_action(message.chat.id, "typing")
           K = []  
           is_chat = chatai.find({"word": message.sticker.file_unique_id})                 
           for x in is_chat:
               K.append(x['text'])
           hey = random.choice(K)
           is_text = chatai.find_one({"text": hey})
           Yo = is_text['check']
           if Yo == "text":
               await message.reply_text(f"{hey}")
           if not Yo == "text":
               await message.reply_sticker(f"{hey}")

@bot.on_message(
    (filters.animation | filters.sticker)
    & filters.private
    & ~filters.bot,
)
async def alexaprivategif(client: Client, message: Message):

    chatdb = MongoClient(MONGO_URL)
    chatai = chatdb["Word"]["WordDb"]

    if not message.reply_to_message:
        await bot.send_chat_action(message.chat.id, "typing")
        K = []
        if message.animation:
            is_chat = chatai.find({"word": message.animation.file_unique_id})
        for x in is_chat:
            K.append(x["text"])
        hey = random.choice(K)
        is_text = chatai.find_one({"text": hey})
        Yo = is_text["check"]
        if Yo == "text":
            await message.reply_text(f"{hey}")
        if not Yo == "text":
            await message.reply_animation(f"{hey}")
        if message.animation:
            chatai.insert_one(
                {
                    "word": message.animation.file_unique_id,
                    "text": message.animation.file_id,
                    "check": "animation",
                }
            )
    if message.reply_to_message:
        getme = await bot.get_me()
        bot_id = getme.id
        if message.reply_to_message.from_user.id == bot_id:
            await bot.send_chat_action(message.chat.id, "typing")
            K = []
            if message.animation:
                is_chat = chatai.find({"word": message.animation.file_unique_id})
            for x in is_chat:
                K.append(x["text"])
            hey = random.choice(K)
            is_text = chatai.find_one({"text": hey})
            Yo = is_text["check"]
            if Yo == "text":
                await message.reply_text(f"{hey}")
            if not Yo == "text":
                await message.reply_animation(f"{hey}")


       
bot.run()
