import discord
from discord.ext import commands, tasks
from discord.utils import get


import asyncio
import time
import datetime
import sys
import json
import os
import logging
import utils

from secret import TOKEN

auto_id = 154428278302703616
kuaj_id = 189489874645155841
mob_id = 198530702558494720

bot_ids = [728962844158328883, 453117389802831882]

authorized_ids = [auto_id, kuaj_id, mob_id]

token = TOKEN

description = 'Soundboard des Cons'
intents = discord.Intents.default()
intents.members = True  # Subscribe to the privileged members intent.
client = commands.Bot(command_prefix='!', intents=intents, description=description)


#client = commands.Bot(command_prefix='!', description=description)

server_name = 'Le Think Tank'
default_role = "Complotiste"


def setup_logging():
    logging.getLogger('discord').setLevel(logging.WARNING)

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)


class UnAuthorized(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def check_auth(message):
    if not message.author.id in authorized_ids:
        logging.warning(f"{message.author.id} - {message.author.name} has tried a command with insufficient permissions")
        raise UnAuthorized('This command requires privileged rights')


def is_admin():
    def predicate(ctx):
        return ctx.message.author.id in authorized_ids
    return commands.check(predicate)


@client.event
async def on_ready():
    try:
        client.general_chan = discord.utils.get(
            client.get_all_channels(), guild__name=server_name, name="general")
        client.test_chan = client.get_channel(239407287091986432)
        client.guild = client.get_guild(198534713575473152)

        client.samples = utils.load_json("samples.json")
        logging.info("Ready !")
        await client.change_presence(status=discord.Status.online, activity=discord.Game('!soundboard'))
        client.aut0wash_DM_channel = client.get_user(154428278302703616)
        await client.aut0wash_DM_channel.send("Hey je suis connecté !")
    except Exception as e:
        logging.error('Error in on_ready: {}'.format(e))


@client.event
async def on_member_join(member):
    try:
        role = discord.utils.get(member.guild.roles, name=default_role)
        await member.add_roles(role)
        logging.info("Added role for new member")
    except Exception as e:
        logging.error('Error in on_member_join: {}'.format(e))


@client.event
async def on_reaction_add(reaction, user):
    try:
        pass
    except Exception as e:
        logging.error('Error in on_reaction_add: {}'.format(e))


@client.event
async def on_voice_state_update(member, before, after):
    try:
        pass
    except Exception as e:
        logging.error('Error in on_voice_state_update: {}'.format(e))


if __name__ == "__main__":
    try:
        setup_logging()
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                client.load_extension(f'cogs.{filename[:-3]}')
        client.run(token)
    except Exception as e:
        logging.error('Error in __main__: {}'.format(e))
