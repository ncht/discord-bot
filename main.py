import discord
import random
import psn
import asyncio
from setting import setting

command_prefix = "!"

client = discord.Client()

def create_psn_message(psn_id, user_state):
    msg = psn_id + "は"

    if user_state == None:
        msg = msg + "だれ？"
    elif user_state["onlineStatus"] != "online":
        msg = msg + "オフライン"
    else:
        if "titleName" not in user_state:
            msg = msg + "オンライン@" + user_state["platform"]
        else:
            msg = msg + user_state["titleName"] + "@" + user_state["platform"] + "をプレイ中"

    return msg

async def psn_task():
    await client.wait_until_ready()

    channel = discord.Object(id=setting["psn_ch"])

    users = setting["psn_users"]

    prev_msg = {}
    for k in users:
        prev_msg[k] = None

    while not client.is_closed:
        for user in users:
            user_state = psn.get_user_state(user)
            msg = create_psn_message(user, user_state)
            if prev_msg[user] == None or msg != prev_msg[user].content:
                if prev_msg[user] != None:
                    await client.delete_message(prev_msg[user])

                prev_msg[user] = await client.send_message(channel, msg)
        await asyncio.sleep(60)

@client.event
async def on_ready():
    print("Logged in")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if not message.content.startswith(command_prefix):
        return
    
    command_and_args = message.content.lstrip(command_prefix).split(maxsplit=1)
    command = command_and_args[0]
    args = None
    if len(command_and_args) > 1:
        args = command_and_args[1]

    if (command == "ps_state"):
        psn_id = None
        if (args == None):
            psn_id = message.author.name
        else:
            psn_id = args
        user_state = psn.get_user_state(psn_id)
        msg = create_psn_message(psn_id, user_state)

        await client.send_message(message.channel, msg)

if __name__ == "__main__":
    client.loop.create_task(psn_task())
    client.run(setting["bot_token"])
