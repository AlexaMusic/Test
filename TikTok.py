import os
import requests
import asyncio
from pyrogram.types import Message
from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

API_ID = int(os.environ.get("API_ID", None))
API_HASH = os.environ.get("API_HASH", None) 
MONGO_DB = os.environ.get("MONGO_DB", None)
LOG_GROUP = int(os.environ.get("LOG_GROUP", None))
SESSION_NAME = os.environ.get("SESSION_NAME", None) 

userbot = Client(
    api_id=API_ID,
    api_hash=API_HASH,
    session_name=SESSION_NAME,
)

mongo_client = MongoClient(MONGO_DB)
db = mongo_client["approved_users_db"]
approved_users_collection = db["approved_users"]

CMD_HANDLER = [".", "/"]
WARNING_LIMIT = 3
JHANTO_LOG_WORD = ["lamd", "bc", "madarchod"]


def is_approved(user_id):
    return approved_users_collection.find_one({"user_id": user_id})

def add_approved_user(user_id):
    approved_users_collection.insert_one({"user_id": user_id, "message_count": 0})

def remove_approved_user(user_id):
    approved_users_collection.delete_one({"user_id": user_id})

def get_user_message_count(user_id):
    user_document = approved_users_collection.find_one({"user_id": user_id})
    if user_document is None:
        return 0
    return user_document.get("message_count", 0)

def increment_user_message_count(user_id):
    user_document = approved_users_collection.find_one({"user_id": user_id})
    if user_document is None:
        add_approved_user(user_id)
        user_document = {"user_id": user_id, "message_count": 0}
    user_document["message_count"] += 1
    approved_users_collection.replace_one({"user_id": user_id}, user_document)

@userbot.on_message(
    ~filters.me & filters.private & ~filters.bot & filters.incoming, group=69
)
async def handle_message(client: userbot, message: Message):
    user_id = message.chat.id
    sender_name = message.from_user.first_name
    user_msg = message.text
    user_unme = message.from_user.username
    await userbot.send_message(LOG_GROUP, f"{sender_name} send a message it's username {user_unme}: {user_msg}")
    text = message.text.lower()
    if any(word in text for word in JHANTO_LOG_WORD):
        await userbot.block_user(user_id)
        await message.reply("You have been blocked for using inappropriate language.")
        return
    increment_user_message_count(user_id)
    message_count = get_user_message_count(user_id)    
    if message_count >= WARNING_LIMIT:
        await message.reply(f"Warning! You have sent {message_count} messages. You will be blocked after {WARNING_LIMIT} messages.")    
    if message_count >= WARNING_LIMIT + 1:
        await userbot.block_user(user_id)
        await message.reply("You have been blocked for sending too many messages.")
        return        
    if not is_approved(user_id):
        await message.reply("You are not an approved user.")

                
@userbot.on_message(
    filters.command(["a", "approve"], CMD_HANDLER) & filters.me & filters.private
)
def approve_command_handler(client: userbot, message: Message):
    user_id = message.chat.id
    if is_approved(user_id):
        message.reply("You are already an approved user.")
    else:
        add_approved_user(user_id)
        message.reply("You have been approved as an authorized user.")
    message.delete()

@userbot.on_message(
    filters.command(["d", "disapprove"], CMD_HANDLER) & filters.me & filters.private
)
def disapprove_command_handler(client: userbot, message: Message):
    user_id = message.chat.id
    if not is_approved(user_id):
        message.reply("You are not an approved user.")
    else:
        remove_approved_user(user_id)
        message.reply("You have been disapproved and removed from the authorized users list.")
    message.delete()

userbot.run()