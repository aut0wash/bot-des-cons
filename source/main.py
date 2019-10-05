import discord
import asyncio
import time
import datetime
import pytz  # pip
import sys
import requests
import json
import os

import logging
from logging_ldp.formatters import LDPGELFFormatter
from logging_ldp.handlers import LDPGELFTCPSocketHandler


token = sys.argv[1]
token_ldp = sys.argv[2]
token_mdp = sys.argv[3]
client = discord.Client()

authorized_id = 189489874645155841
bot_id = 453117389802831882
server_name = 'Le Discord des Cons'
bot_channel = 'logs'
access_logs = None
general = None
default_role = "Trou du cul la balayette"


def setup_logging():
    handler = LDPGELFTCPSocketHandler(hostname="gra1.logs.ovh.com")
    handler.setFormatter(LDPGELFFormatter(token=token_ldp))
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.INFO)
    logging.getLogger('discord').setLevel(logging.WARNING)


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
        logging.warning('{} is tried a command with insufficient permission'.format(message.author.id))
        raise UnAuthorized('This command requires privileged rights')


class Metric:
    def __init__(self):
        self.url = 'https://warp10.romain-dupont.fr/api/v0/update'
        self.headers = {'X-Warp10-Token': token_mdp,
                        'content-type': 'text/plain'}
        self.metric_time = int(time.time()) * 1000000


class MetricConnection(Metric):
    def __init__(self, channel_name):
        super().__init__()
        self.channel_name = channel_name
        self.metric_name = "discord.events.connection"

    def push(self, direction):
        payload = "{}// {}{{direction={},channel={}}} 1".format(
            self.metric_time,
            self.metric_name,
            direction,
            self.channel_name        
        )
        logging.info("sending payload {}".format(payload))
        requests.post(
            self.url,
            headers=self.headers,
            data=payload
        )


class MetricNewMember(Metric):
    def __init__(self):
        super().__init__()
        self.metric_name = "discord.events.new.member"

    def push(self):
        payload = "{}// {}{{}} 1".format(
            self.metric_time,
            self.metric_name
        )
        logging.info("sending payload {}".format(payload))
        requests.post(
            self.url,
            headers=self.headers,
            data=payload
        )


class MetricNewMessage(Metric):
    def __init__(self, channel):
        super().__init__()
        self.channel = channel
        self.metric_name = "discord.events.new.message"

    def push(self):
        payload = "{}// {}{{channel={}}} 1".format(
            self.metric_time,
            self.metric_name,
            self.channel
        )
        logging.info("sending payload {}".format(payload))
        requests.post(
            self.url,
            headers=self.headers,
            data=payload
        )


@client.event
async def on_ready():
    try:
        global access_logs
        access_logs = discord.utils.get(
            client.get_all_channels(),
            guild__name=server_name,
            name=bot_channel
        )
        global general
        general = discord.utils.get(
            client.get_all_channels(),
            guild__name=server_name,
            name="general"
        )
    except Exception as e:
        logging.error('Error in on_ready: {}'.format(e))


@client.event
async def on_member_join(member):
    try:
        role = discord.utils.get(
            member.guild.roles,
            name=default_role
        )
        await member.add_roles(role)
        MetricNewMember().push()
        logging.info("Added role for new member")
    except Exception as e:
        logging.error('Error in on_member_join: {}'.format(e))


@client.event
async def on_message(message):
    try:
        if not message.author.id == bot_id and type(message.channel) == discord.channel.DMChannel:
            check_auth(message)
            await general.send(message.content)
        if not message.author.id == bot_id and not type(message.channel) == discord.channel.DMChannel:
            MetricNewMessage(message.channel.name).push()
    except Exception as e:
        loggin.error('Error in on_message: {}'.format(e))


@client.event
async def on_reaction_add(reaction, user):
    pass


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

        if before_channel is None and after_channel is not None:
            payload = '```diff\n+ {} IN  {}\n```'.format(get_time(), name)
            await access_logs.send(payload)
            MetricConnection(after_channel.name).push("in")
        elif after_channel is None and before_channel is not None:
            payload = '```diff\n- {} OUT  {}\n```'.format(get_time(), name)
            await access_logs.send(payload)
            MetricConnection("None").push("out")
    except Exception as e:
        logging.error('Error in on_voice_state_update: {}'.format(e))

if __name__ == "__main__":
    try:
        setup_logging()
        client.run(token)
    except Exception as e:
        logging.error('Error in __main__: {}'.format(e))
