import os
import requests
import asyncio
from pyrogram.types import Message
from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

API_ID = os.environ.get("API_ID", None) 
API_HASH = os.environ.get("API_HASH", None) 
MONGO_DB = os.environ.get("MONGO_DB", None)
LOG_ID = os.environ.get("LOG_ID", None)
SESSION_NAME = os.environ.get("SESSION_NAME", None) 

client = Client(SESSION_NAME, API_ID, API_HASH)

mongo_client = MongoClient(MONGO_DB)
db = mongo_client["approved_users_db"]
approved_users_collection = db["approved_users"]

WARNING_LIMIT = 3
JHANTO_LOG_WORD = ["lamd", "bc", "madarchod"]


def is_approved(user_id):
    return approved_users_collection.find_one({"user_id": user_id}) is not None

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

def block_user(user_id):
    client.block_user(user_id)

@Client.on_message(filters.private)
def handle_message(client, message):
    user_id = message.from_user.id
    log_channel = client.get_chat(LOG_ID)
    user_first_name = message.from_user.first_name
    log_message = f"{user_first_name}: {message.text}"
    log_channel.send(log_message)
    if not is_approved(user_id):
        message.reply("You are not an approved user.")
        return
    text = message.text.lower()
    if any(word in text for word in JHANTO_LOG_WORD):
        block_user(user_id)
        message.reply("You have been blocked for using inappropriate language.")
        return
    increment_user_message_count(user_id)
    message_count = get_user_message_count(user_id)    
    if message_count >= WARNING_LIMIT:
        message.reply(f"Warning! You have sent {message_count} messages. You will be blocked after {WARNING_LIMIT} messages.")    
    if message_count >= WARNING_LIMIT + 1:
        block_user(user_id)
        message.reply("You have been blocked for sending too many messages.")
    message.delete()
        
@Client.on_message(filters.command("approve")  & filters.me)
def approve_command_handler(client, message):
    user_id = message.from_user.id
    if is_approved(user_id):
        message.reply("You are already an approved user.")
        return
    add_approved_user(user_id)
    message.reply("You have been approved as an authorized user.")

@Client.on_message(filters.command("disapprove") & filters.me)
def disapprove_command_handler(client, message):
    user_id = message.from_user.id
    if not is_approved(user_id):
        message.reply("You are not an approved user.")
        return
    remove_approved_user(user_id)
    message.reply("You have been disapproved and removed from the authorized users list.")


client.run()