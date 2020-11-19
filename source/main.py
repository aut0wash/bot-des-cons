import discord
from discord.ext import commands, tasks

import asyncio
import time
import datetime
import sys
import json
import os
import logging
import utils

auto_id = 154428278302703616
kuaj_id = 189489874645155841
mob_id = 198530702558494720

bot_ids = [728962844158328883, 453117389802831882]

authorized_ids = [auto_id, kuaj_id, mob_id]

token = sys.argv[1]

description = "Soundboard des Cons"

intents = discord.Intents.default()
intents.members = True  # Subscribe to the privileged members intent.
client = commands.Bot(command_prefix='!', intents=intents, description=description)

server_name = "Le Think Tank"
default_role = 295466109698703362  # Complotiste


def setup_logging():
    logging.getLogger("discord").setLevel(logging.WARNING)

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    root.addHandler(handler)


class UnAuthorized(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def check_auth(message):
    if not message.author.id in authorized_ids:
        logging.warning(
            f"{message.author.id} - {message.author.name} has tried a command with insufficient permissions")
        raise UnAuthorized("This command requires privileged rights")


def is_admin():
    def predicate(ctx):
        return ctx.message.author.id in authorized_ids
    return commands.check(predicate)


@client.event
async def on_ready():
    try:
        client.general_chan = discord.utils.get(
            client.get_all_channels(), guild__name=server_name, name="general")
        client.guild = client.get_guild(198534713575473152)
        client.samples = utils.load_json("samples.json")
        # link = await client.general_chan.create_invite(max_age=0, max_uses=1, unique=True)
        # logging.info(f"Invitation link: {link}")
        role = discord.utils.get(client.guild.roles, id=default_role)
        logging.info(
            f"Checking that everyone has at least the default role {role}")
        for member in client.guild.members:
            if len(member.roles) == 1:
                await member.add_roles(role)
                logging.info(f"Added role {role} for {member.display_name}")
        logging.info("Ready !")
    except Exception as e:
        logging.error(f"Error in on_ready: {e}")


@client.event
async def on_member_join(member):
    try:
        await member.add_roles(discord.utils.get(member.guild.roles, id=default_role))
        logging.info("Added role for new member")
    except Exception as e:
        logging.error(f"Error in on_member_join: {e}")


@client.event
async def on_reaction_add(reaction, user):
    try:
        pass
    except Exception as e:
        logging.error(f"Error in on_reaction_add: {e}")


@client.event
async def on_voice_state_update(member, before, after):
    try:
        pass
    except Exception as e:
        logging.error(f"Error in on_voice_state_update: {e}")

if __name__ == "__main__":
    try:
        setup_logging()
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                client.load_extension(f"cogs.{filename[:-3]}")
        client.run(token)
    except Exception as e:
        logging.error(f"Error in __main__: {e}")
