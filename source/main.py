import discord
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

bot_ids = [728962844158328883, 453117389802831882]

authorized_ids = [auto_id, kuaj_id]

token = sys.argv[1]
client = discord.Client()

server_name = 'Le Discord des Cons'
default_role = "Trou du cul la balayette"


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


@client.event
async def on_ready():
    try:
        client.general_chan = discord.utils.get(
            client.get_all_channels(), guild__name=server_name, name="general")
        client.test_chan = client.get_channel(239407287091986432)
        client.guild = client.get_guild(198534713575473152)

        client.samples = utils.load_json("samples.json")

        logging.info("Ready !")
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
async def on_message(message):
    try:
        logging.info('Message from {0.author}: {0.content}'.format(message))
        if type(message.channel) == discord.channel.DMChannel and message.author.id not in bot_ids:
            check_auth(message)

            sample = utils.get_sample_from_name(
                client.samples, message.content)
            if sample:
                member = client.guild.get_member(message.author.id)
                connected = member.voice
                if connected:
                    vc = await connected.channel.connect()
                    vc.play(discord.FFmpegPCMAudio(f"/root/discord/{sample.path}", options=f"-vol {sample.volume}"), after=lambda e: logging.info(f"Finished, {e}"))

                    while vc.is_playing():
                        await asyncio.sleep(0.5)
                    await vc.disconnect()

            if message.content == "help":
                command_list = []
                for sample in client.samples:
                    command_list.append(client.samples[sample]["name"])
                await message.channel.send(command_list)
    except Exception as e:
        logging.error('Error in on_message: {}'.format(e))


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
        client.run(token)
    except Exception as e:
        logging.error('Error in __main__: {}'.format(e))
