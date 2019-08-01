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
client = discord.Client()

authorized_id = 189489874645155841
bot_id = 453117389802831882
server_name = 'Le Discord des Cons'
bot_channel = 'logs'
access_logs = None
general = None
postmatch_channel = 'post_match'
postmatch = None


def setup_logging():
    handler = LDPGELFTCPSocketHandler(hostname="gra1.logs.ovh.com")
    handler.setFormatter(LDPGELFFormatter(token=token_ldp))
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.INFO)


def JSONRequester(URL):
    r = requests.get(URL)

    json_data = json.loads(r.text)
    j = json.dumps(json_data, ensure_ascii=False)
    JSON = json.loads(j)

    return JSON


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
        logging.info(server_name)
        global access_logs
        access_logs = discord.utils.get(
            client.get_all_channels(), guild__name=server_name, name=bot_channel)
        global general
        general = discord.utils.get(
            client.get_all_channels(), guild__name=server_name, name="general")
        global postmach
        postmach = discord.utils.get(client.get_all_channels(
        ), guild__name=server_name, name=postmatch_channel)
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
            print('printing message to general : {}'.format(message.content))
            await general.send(message.content)

    except Exception as e:
        print('Error in on_message: {}'.format(e))

    try:
        command = '!counter'
        ms = str.lower(message.content)
        if message.channel.name == postmatch_channel and ms.startswith(command):
            try:
                with open("datahero.json", "r") as jsonFile:
                    hereos_data = json.load(jsonFile)
                sp_pos1 = ms.find(' ', len(command)-1)
                hero_name_input = ms[sp_pos1+1:]
                hero_name = str.lower(hero_name_input.replace(' ', ''))
                h = -1
                finish = False
                while finish is False:
                    for i in range(len(hereos_data)):
                        h = h+1
                        name = -1
                        for n in range(len(hereos_data[h]["used_names"])):
                            name = name+1
                            if hereos_data[h]["used_names"][name] == hero_name:
                                heroid = hereos_data[h]["id"]
                                herolocalisedname = hereos_data[h]["localized_name"]
                                if hero_name == str.lower(herolocalisedname):
                                    surnom = ''
                                else:
                                    surnom = ' AKA {}'.format(
                                        str.capitalize(hero_name_input))
                                await postmach.send('Checking stats for counter {}{}, please wait...'.format(hereos_data[h]["localized_name"], surnom))
                                finish = True
                                break
                                # sortir de la boucle for i in range(len(hereos_data)) quand le résultat est correct
                            else:
                                pass
                        if i == len(hereos_data):
                            finish = True
                        if finish == True:
                            break
                url = 'https://api.stratz.com/api/v1/Hero/' + \
                    str(heroid) + '/matchUp'
                heromatchup = JSONRequester(url)
                top1counter = heromatchup["disadvantage"][0]["vs"][0]["heroId2"]
                h = -1
                for i in range(len(hereos_data)):
                    h = h+1
                    if hereos_data[h]["id"] == top1counter:
                        top1counter_name = hereos_data[h]["localized_name"]
                top2counter = heromatchup["disadvantage"][0]["vs"][1]["heroId2"]
                h = -1
                for i in range(len(hereos_data)):
                    h = h+1
                    if hereos_data[h]["id"] == top2counter:
                        top2counter_name = hereos_data[h]["localized_name"]
                top3counter = heromatchup["disadvantage"][0]["vs"][2]["heroId2"]
                h = -1
                for i in range(len(hereos_data)):
                    h = h+1
                    if hereos_data[h]["id"] == top3counter:
                        top3counter_name = hereos_data[h]["localized_name"]
                top4counter = heromatchup["disadvantage"][0]["vs"][3]["heroId2"]
                h = -1
                for i in range(len(hereos_data)):
                    h = h+1
                    if hereos_data[h]["id"] == top4counter:
                        top4counter_name = hereos_data[h]["localized_name"]
                top5counter = heromatchup["disadvantage"][0]["vs"][4]["heroId2"]
                h = -1
                for i in range(len(hereos_data)):
                    h = h+1
                    if hereos_data[h]["id"] == top5counter:
                        top5counter_name = hereos_data[h]["localized_name"]

                await postmach.send('Top counterpicks against {}{} :\n:first_place:- {} \n:second_place:- {} \n:third_place:- {} \n  4   - {} \n  5   - {}'.format(herolocalisedname, surnom, top1counter_name, top2counter_name, top3counter_name, top4counter_name, top5counter_name))
            except:
                await postmach.send('Invalid command, please try again : !command')
        # else:
            # f=0
    except Exception as e:
        print('Error in on_message: {}'.format(e))

    try:
        command = '!my'  # my hero
        ms = str.lower(message.content)
        if message.channel.name == postmatch_channel and ms.startswith(command):
            try:
                with open("bdd.json", "r") as jsonFile:
                    bdd = json.load(jsonFile)
                discordId = message.author.id
                steamId = bdd[str(discordId)]["steamId"]
                with open("datahero.json", "r") as jsonFile:
                    hereos_data = json.load(jsonFile)
                sp_pos1 = ms.find(' ', len(command)-1)
                hero_name_input = ms[sp_pos1+1:]
                hero_name = str.lower(hero_name_input.replace(' ', ''))
                h = -1
                finish = False
                while finish is False:
                    for i in range(len(hereos_data)):
                        h = h+1
                        name = -1
                        for n in range(len(hereos_data[h]["used_names"])):
                            name = name+1
                            if hereos_data[h]["used_names"][name] == hero_name:
                                heroid = hereos_data[h]["id"]
                                herolocalisedname = hereos_data[h]["localized_name"]

                                await postmach.send('Checking your stats with {}, please wait...'.format(hereos_data[h]["localized_name"]))
                                finish = True
                                break
                                # sortir de la boucle for i in range(len(hereos_data)) quand le résultat est correct
                            else:
                                pass
                        if i == len(hereos_data):
                            finish = True
                        if finish == True:
                            break
                url = 'https://api.opendota.com/api/players/' + \
                    str(steamId) + '/heroes'
                opendotaplayersherostats = JSONRequester(url)
                for hero in range(len(opendotaplayersherostats)):
                    if opendotaplayersherostats[hero]['hero_id'] == str(heroid):
                        lastgame = opendotaplayersherostats[hero]['last_played']
                        gamescount = opendotaplayersherostats[hero]['games']
                        winscount = opendotaplayersherostats[hero]['win']
                        winrate = round(((winscount/gamescount) * 100), 1)
                        if winrate >= 55:
                            com_win = ':quandmeme:'
                        elif winrate >= 50 and winrate < 55:
                            com_win = ':thumbsup:'
                        elif winrate < 50 and winrate >= 45:
                            com_win = ':thumbsdown:'
                        else:
                            com_win = ':malaise:'
                        withgames = opendotaplayersherostats[hero]['with_games']
                        winwith = opendotaplayersherostats[hero]['with_win']
                        winratewith = round(((winwith/withgames) * 100), 1)
                        againstgames = opendotaplayersherostats[hero]['against_games']
                        winagainst = opendotaplayersherostats[hero]['against_win']
                        winrateagainst = round(
                            ((winagainst/againstgames) * 100), 1)

                url = 'https://api.stratz.com/api/v1/Player/' + \
                    str(steamId) + '/heroPerformance/' + str(heroid)
                stratzplayersherostats = JSONRequester(url)
                currentstreak = stratzplayersherostats['streak']
                maxstreak = stratzplayersherostats['maxStreak']
                if currentstreak == maxstreak:
                    com_streak = ':PogChamp:'
                if maxstreak - currentstreak <= 2 and maxstreak > 5:
                    com_streak = "you're not so far !"
                if currentstreak == 1:
                    com_streak = "it's still better than a lose..."
                if currentstreak == 0:
                    com_streak = "well, you should maybe change hero..."
                avgkills = round(stratzplayersherostats['avgNumKills'], 1)
                maxkills = stratzplayersherostats['maxNumKills']
                avgdeaths = round(stratzplayersherostats['avgNumDeaths'], 1)
                mindeaths = stratzplayersherostats['maxNumDeaths']
                avgassists = round(stratzplayersherostats['avgNumAssists'], 1)
                maxassists = stratzplayersherostats['maxNumAssists']
                avggpm = round(stratzplayersherostats['avgGoldPerMinute'])
                maxgpm = round(stratzplayersherostats['maxGoldPerMinute'])
                avgxpm = round(
                    stratzplayersherostats['avgExperiencePerMinute'])
                maxxpm = round(
                    stratzplayersherostats['maxExperiencePerMinute'])
                avglh = round(stratzplayersherostats['avgNumLastHits'])
                maxlh = stratzplayersherostats['maxNumLastHits']
                await postmach.send('Your statistics with **{}** in **{}** games :\n {}   {}% win\n {} games played with ({}% win)\n {} games played against ({}% win)\n            __Records :__\n      Kills : {} (*{}*)\n      Deaths : {} (*{}*)\n      Assists : {} (*{}*)\n      GPM : {} (*{}*)\n      XPM : {} (*{}*)\n      Last-hits : {} (*{}*)\n\n Your winning streak is {} and your record is {} : {}'.format(herolocalisedname, gamescount, com_win, winrate, withgames, winratewith, againstgames, winrateagainst, avgkills, maxkills, avgdeaths, mindeaths, avgassists, maxassists, avggpm, maxgpm, avgxpm, maxxpm, avglh, maxlh, currentstreak, maxstreak, com_streak))
            except:
                await postmach.send('Invalid command, please try again : !command')
        # else:
            # f=0
    except Exception as e:
        print('Error in on_message: {}'.format(e))

    try:
        command = '!his'  # his pseudo - héro
        ms = str.lower(message.content)
        if message.channel.name == postmatch_channel and ms.startswith(command):
            try:
                sp_pos1 = ms.find(' ', len(command)-1)
                sp_pos2 = ms.find(' ', sp_pos1+1)
                username = ms[sp_pos1+1:sp_pos2]
                with open("bdd.json", "r") as jsonFile:
                    bdd = json.load(jsonFile)
                for user in bdd:
                    if bdd[user]['name'] == username:
                        discordId = user
                        steamId = bdd[user]["steamId"]
                with open("datahero.json", "r") as jsonFile:
                    hereos_data = json.load(jsonFile)
                tiret_pos1 = ms.find('-', len(command)+len(username)-1)
                hero_name_input = ms[tiret_pos1+1:]
                hero_name = str.lower(hero_name_input.replace(' ', ''))
                h = -1
                finish = False
                while finish is False:
                    for i in range(len(hereos_data)):
                        h = h+1
                        name = -1
                        for n in range(len(hereos_data[h]["used_names"])):
                            name = name+1
                            if hereos_data[h]["used_names"][name] == hero_name:
                                heroid = hereos_data[h]["id"]
                                herolocalisedname = hereos_data[h]["localized_name"]

                                await postmach.send("Checking {}'s stats with {}, please wait...".format(str.capitalize(username), hereos_data[h]["localized_name"]))
                                finish = True
                                break
                                # sortir de la boucle for i in range(len(hereos_data)) quand le résultat est correct
                            else:
                                pass
                        if i == len(hereos_data):
                            finish = True
                        if finish == True:
                            break
                url = 'https://api.opendota.com/api/players/' + \
                    str(steamId) + '/heroes'
                opendotaplayersherostats = JSONRequester(url)
                for hero in range(len(opendotaplayersherostats)):
                    if opendotaplayersherostats[hero]['hero_id'] == str(heroid):
                        lastgame = opendotaplayersherostats[hero]['last_played']
                        gamescount = opendotaplayersherostats[hero]['games']
                        winscount = opendotaplayersherostats[hero]['win']
                        winrate = round(((winscount/gamescount) * 100), 1)
                        if winrate >= 55:
                            com_win = ':quandmeme:'
                        elif winrate >= 50 and winrate < 55:
                            com_win = ':thumbsup:'
                        elif winrate < 50 and winrate >= 45:
                            com_win = ':thumbsdown:'
                        else:
                            com_win = ':malaise:'
                        withgames = opendotaplayersherostats[hero]['with_games']
                        winwith = opendotaplayersherostats[hero]['with_win']
                        winratewith = round(((winwith/withgames) * 100), 1)
                        againstgames = opendotaplayersherostats[hero]['against_games']
                        winagainst = opendotaplayersherostats[hero]['against_win']
                        winrateagainst = round(
                            ((winagainst/againstgames) * 100), 1)

                url = 'https://api.stratz.com/api/v1/Player/' + \
                    str(steamId) + '/heroPerformance/' + str(heroid)
                stratzplayersherostats = JSONRequester(url)
                currentstreak = stratzplayersherostats['streak']
                maxstreak = stratzplayersherostats['maxStreak']
                if currentstreak == maxstreak:
                    com_streak = ':PogChamp:'
                if maxstreak - currentstreak <= 2 and maxstreak > 5:
                    com_streak = "He isn't so far !"
                if currentstreak == 1:
                    com_streak = "it's still better than a lose..."
                if currentstreak == 0:
                    com_streak = "well, he should maybe change hero..."
                avgkills = round(stratzplayersherostats['avgNumKills'], 1)
                maxkills = stratzplayersherostats['maxNumKills']
                avgdeaths = round(stratzplayersherostats['avgNumDeaths'], 1)
                mindeaths = stratzplayersherostats['maxNumDeaths']
                avgassists = round(stratzplayersherostats['avgNumAssists'], 1)
                maxassists = stratzplayersherostats['maxNumAssists']
                avggpm = round(stratzplayersherostats['avgGoldPerMinute'])
                maxgpm = round(stratzplayersherostats['maxGoldPerMinute'])
                avgxpm = round(
                    stratzplayersherostats['avgExperiencePerMinute'])
                maxxpm = round(
                    stratzplayersherostats['maxExperiencePerMinute'])
                avglh = round(stratzplayersherostats['avgNumLastHits'])
                maxlh = stratzplayersherostats['maxNumLastHits']
                await postmach.send('His statistics with **{}** in **{}** games :\n {}   {}% win\n {} games played with ({}% win)\n {} games played against ({}% win)\n            __Records :__\n      Kills : {} (*{}*)\n      Deaths : {} (*{}*)\n      Assists : {} (*{}*)\n      GPM : {} (*{}*)\n      XPM : {} (*{}*)\n      Last-hits : {} (*{}*)\n\n His winning streak is {} and record is {} : {}'.format(herolocalisedname, gamescount, com_win, winrate, withgames, winratewith, againstgames, winrateagainst, avgkills, maxkills, avgdeaths, mindeaths, avgassists, maxassists, avggpm, maxgpm, avgxpm, maxxpm, avglh, maxlh, currentstreak, maxstreak, com_streak))
            except:
                await postmach.send('Invalid command, please try again : !command')
        # else:
            # f=0
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

        if before_channel is None and after_channel is not None:
            await access_logs.send('```diff\n+ {} IN  {}\n```'.format(get_time(), name))
        elif after_channel is None and before_channel is not None:
            await access_logs.send('```diff\n- {} OUT {}\n```'.format(get_time(), name))
    except Exception as e:
        print('Error in on_voice_state_update: {}'.format(e))

if __name__ == "__main__":
    try:
        setup_logging()
        logging.info("Starting bot-des-cons !")
        client.run(token)
    except Exception as e:
        print('Error in __main__: {}'.format(e))
