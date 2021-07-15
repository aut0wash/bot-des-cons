import discord
from discord.ext import commands, tasks
from discord.utils import get


import utils

from secret import TOKEN

auto_id = 154428278302703616
kuaj_id = 189489874645155841
mob_id = 198530702558494720

server_name = 'Le Discord des Cons'
default_role = "Cons en devenir"

token = TOKEN

description = 'Soundboard des Cons'
intents = discord.Intents.default()
intents.members = True  # Subscribe to the privileged members intent.
client = commands.Bot(command_prefix='!', intents=intents, description=description)

@client.event
async def on_ready():
    try:
        client.aut0wash_DM_channel = client.get_user(154428278302703616)
        await client.aut0wash_DM_channel.send("Hey je suis connecté !")
    except Exception as e:
        print(e)

client.run(token)