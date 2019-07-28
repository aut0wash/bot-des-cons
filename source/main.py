import discord
import asyncio
import time
import datetime
import pytz  # pip
import sys


token = sys.argv[1]
client = discord.Client()
authorized_id = 189489874645155841
bot_id = 453117389802831882
server_name = 'Le Discord des Cons'
bot_channel = 'logs'
access_logs = None
general = None


class UnAuthorized(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def get_time():
    tz = pytz.timezone('Europe/Berlin')
    berlin_now = datetime.datetime.now(tz)
    return berlin_now.strftime('%d-%m-%Y %H:%M:%S')


def check_auth(message):
    if not message.author.id == authorized_id:
        raise UnAuthorized('This command requires privileged rights')


@client.event
async def on_ready():
    try:
        print(server_name)
        global access_logs
        access_logs = discord.utils.get(
            client.get_all_channels(), guild__name=server_name, name=bot_channel)
        global general
        general = discord.utils.get(
            client.get_all_channels(), guild__name=server_name, name="general")
    except Exception as e:
        print('Error in on_ready: {}'.format(e))


@client.event
async def on_member_join(member):
    try:
        role = discord.utils.get(
            member.server.roles, name="Trou du cul la balayette")
        await client.add_roles(member, role)
    except Exception as e:
        print('Error in on_member_join: {}'.format(e))


@client.event
async def on_message(message):
    try:
        if not message.author.id == bot_id and type(message.channel) == discord.channel.DMChannel:
            check_auth(message)
            print('printing message to general:')
            await general.send(message.content)

    except Exception as e:
        print('Error in on_message: {}'.format(e))


@client.event
async def on_voice_state_update(member, before, after):
    try:
        before_channel = before.channel
        after_channel = after.channel
        if before_channel:
            if before_channel.name == 'Accueil':
                before_channel = None
        if after_channel:
            if after_channel.name == 'Accueil':
                after_channel = None
        name = member.name
        if not member.display_name == member.name:
            name = member.name+' aka '+member.display_name

        if before_channel == None and not after_channel == None:
            await access_logs.send('```diff\n+ {} IN  {}\n```'.format(get_time(), name))
        elif after_channel == None and not before_channel == None:
            await access_logs.send('```diff\n- {} OUT {}\n```'.format(get_time(), name))
    except Exception as e:
        print('Error in on_voice_state_update: {}'.format(e))

if __name__ == "__main__":
    try:
        client.run(token)
    except Exception as e:
        print('Error in __main__: {}'.format(e))

