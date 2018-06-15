import discord
import asyncio
import time
import datetime
import pytz #pip
import sys


token           = sys.argv[1]
client          = discord.Client()
authorized_id   = '189489874645155841'
bot_id          = '453117389802831882'
server_name     = 'Le Discord des Cons'
bot_channel     = 'logs'
access_logs     = None
general         = None


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
        print(message.author.id)
        print(message.content)
        raise UnAuthorized('This command requires privileged rights')


@client.event
async def on_ready():
    print(server_name)
    global access_logs
    access_logs = discord.utils.get(client.get_all_channels(), server__name=server_name, name=bot_channel)
    global general
    general = discord.utils.get(client.get_all_channels(), server__name=server_name, name="general")


@client.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, name="Trou du cul la balayette")
    await client.add_roles(member, role)


@client.event
async def on_message(message):
    try:
        if not message.author.id == bot_id and message.channel.is_private:
            check_auth(message)
            print('printing message to general:')
            await client.send_message(general, message.content)

    except Exception as e:
        print('Error in on_message: '+str(e))


@client.event
async def on_voice_state_update(before, after):
    try:
        before_channel = before.voice.voice_channel
        after_channel = after.voice.voice_channel
        if before_channel:
            if before_channel.name == 'Accueil':
                before_channel = None
        if after_channel:
            if after_channel.name == 'Accueil':
                after_channel = None
        name = before.name
        if not before.display_name == before.name:
            name = before.name+' aka '+before.display_name

        if before_channel == None and not after_channel == None:
            await client.send_message(access_logs, '```diff\n+ '+get_time()+' IN  '+name+'\n```')
        elif after_channel == None and not before_channel == None:
            await client.send_message(access_logs, '```diff\n- '+get_time()+' OUT '+name+'\n```')

    except Exception as e:
        print('Error in on_voice_state_update : '+str(e))

def main():
    try:
        client.run(token)
    except Exception as e:
        print('Error in main: '+str(e))

main()


