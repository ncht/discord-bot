import discord
import random

client = discord.Client()

@client.event
async def on_ready():
    print("Logged in")

@client.event
async def on_message(message):
    emojis = ["👍", "👎"]

    react_num = random.randint(0, len(emojis) - 1)
    await client.add_reaction(message, emojis[react_num])

if __name__ == "__main__":
    client.run("")
