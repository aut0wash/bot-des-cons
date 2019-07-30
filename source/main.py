import requests
import discord
import os
import asyncio
import time
import datetime
import pytz  # pip
import sys
import json
from Levenshtein import ratio

import utilitary as utilitary
import commands as commands
import apiparser as apiparser

token = sys.argv[1]

client = discord.Client()

authorized_id = 189489874645155841
bot_id = 453117389802831882
server_name = 'Le Discord des Cons'
bot_channel = 'logs'
access_logs = None
general = None
postmatch_channel = 'post_match'
postmatch = None


class UnAuthorized(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


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
        global postmatch
        postmatch = discord.utils.get(client.get_all_channels(), guild__name=server_name, name=postmatch_channel)
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
    recc_ratio = 0.60
    recc_name = ''
    simil = 0
    try:
        if not message.author.id == bot_id and type(message.channel) == discord.channel.DMChannel:
            check_auth(message)
            print('printing message to general : {}'.format(message.content))
            await general.send(message.content)

    except Exception as e:
        print('Error in on_message: {}'.format(e))

    try:
        command = ['!command', '!help', '!commands']
        ms = str.lower(message.content)
        for com in command :
            if message.channel.name == postmatch_channel and ms == com:
                try:
                    await postmatch.send("__**Here is the list of the commands :**__ \n**!commands** or **!help** \n**!counter *heroname*** : Give the top 5 against this hero \n**!my *heroname*** : Give some statistics about you and this hero \n**!his *discordname* - *heroname*** : As !my heroname but for someone else \n")
                except:
                    await postmatch.send('Invalid command, please try again : !commands')
                else:
                    f=0
    except Exception as e:
        print('Error in on_message: {}'.format(e))

    try:
        command = '!counter'
        ms = str.lower(message.content)
        if message.channel.name == postmatch_channel and ms.startswith(command):
            try:
                with open("datahero.json", "r") as jsonFile:
                    hereos_data = json.load(jsonFile)
                sp_pos1 = ms.find(' ',len(command)-1)
                hero_name_input = ms[sp_pos1+1:]
                hero_name = str.lower(hero_name_input.replace(' ',''))
                h = -1
                for i in range(len(hereos_data)):
                    h = h+1
                    name = -1
                    for n in range(len(hereos_data[h]["used_names"])):
                        name = name+1
                        if hereos_data[h]["used_names"][name] == hero_name:
                            simil = 1
                            heroid=hereos_data[h]["id"]
                            herolocalisedname = hereos_data[h]["localized_name"]
                            if hero_name == str.lower(herolocalisedname):
                                surnom = ''
                            else :
                                surnom = ' AKA {}'.format(str.capitalize(hero_name_input))
                            await postmatch.send('Checking stats for counter {}{}, please wait...'.format(hereos_data[h]["localized_name"], surnom))
                            break
                            #sortir de la boucle for i in range(len(hereos_data)) quand le résultat est correct
                        else :
                            ratio_hero = ratio(hero_name, hereos_data[h]["used_names"][name])
                            if ratio_hero >= recc_ratio :
                                recc_ratio = ratio_hero
                                last_recc_name = recc_name
                                recc_name = hereos_data[h]["used_names"][name]
                                print(recc_ratio, last_recc_name, recc_name)
                if simil == 0 :
                    print('retry')
                    await postmatch.send("I'm not sure, did you mean {} or {} ?".format(str.capitalize(last_recc_name), str.capitalize(recc_name)))
                else :
                    match_up = apiparser.stratz_matchup(heroid, hereos_data)

                    await postmatch.send('Top counterpicks against {}{} :\n:first_place:- {} \n:second_place:- {} \n:third_place:- {} \n  4   - {} \n  5   - {}'.format(herolocalisedname, surnom, match_up[0], match_up[1], match_up[2], match_up[3], match_up[4]))
            except:
                await postmatch.send('Invalid command, please try again : !command')
        else:
            f=0
    except Exception as e:
        print('Error in on_message: {}'.format(e))

    try:
        command = '!my' #my hero
        ms = str.lower(message.content)
        if message.channel.name == postmatch_channel and ms.startswith(command):
            try:
                with open("bdd.json", "r") as jsonFile:
                    bdd = json.load(jsonFile)
                discordId = message.author.id
                steamId = bdd[str(discordId)]["steamId"]
                with open("datahero.json", "r") as jsonFile:
                    hereos_data = json.load(jsonFile)
                sp_pos1 = ms.find(' ',len(command)-1)
                hero_name_input = ms[sp_pos1+1:]
                hero_name = str.lower(hero_name_input.replace(' ',''))
                h = -1
                finish = False
                while finish is False :
                    for i in range(len(hereos_data)):
                        h = h+1
                        name = -1
                        for n in range(len(hereos_data[h]["used_names"])):
                            name = name+1
                            if hereos_data[h]["used_names"][name] == hero_name:
                                heroid=hereos_data[h]["id"]
                                herolocalisedname = hereos_data[h]["localized_name"]
                                await postmatch.send('Checking your stats with {}, please wait...'.format(hereos_data[h]["localized_name"]))
                                finish = True
                                break
                                #sortir de la boucle for i in range(len(hereos_data)) quand le résultat est correct
                            else :
                                pass
                        if i == len(hereos_data):
                            finish = True
                        if finish == True :
                            break
                opendota_stats = apiparser.opendota_hero_stats(steamId, heroid)
                stratz_stats = apiparser.stratz_hero_stats(steamId, heroid)
                await postmatch.send('Your statistics with **{}** in **{}** games :\n {}   {}% win\n {} games played with ({}% win)\n {} games played against ({}% win)\n            __Records :__\n      Kills : {} (*{}*)\n      Deaths : {} (*{}*)\n      Assists : {} (*{}*)\n      GPM : {} (*{}*)\n      XPM : {} (*{}*)\n      Last-hits : {} (*{}*)\n\n Your winning streak is {} and your record is {} : {}'.format(herolocalisedname, opendota_stats[1], opendota_stats[4], opendota_stats[3], opendota_stats[5], opendota_stats[7], opendota_stats[8], opendota_stats[10], stratz_stats[3], stratz_stats[4], stratz_stats[5], stratz_stats[6], stratz_stats[7], stratz_stats[8], stratz_stats[9], stratz_stats[10], stratz_stats[11], stratz_stats[12], stratz_stats[13], stratz_stats[14], stratz_stats[0], stratz_stats[1],stratz_stats[2]))
            except:
                await postmatch.send('Invalid command, please try again : !command')
        else:
            f=0
    except Exception as e:
        print('Error in on_message: {}'.format(e))

    try:
        command = '!his' #his pseudo - héro
        ms = str.lower(message.content)
        if message.channel.name == postmatch_channel and ms.startswith(command):
            try:
                with open("bdd.json", "r") as jsonFile:
                    bdd = json.load(jsonFile)
                sp_pos1 = ms.find(' ',len(command)-1)
                sp_pos2 = ms.find(' ',sp_pos1+1)
                username =  ms[sp_pos1+1:sp_pos2]
                if username.startswith('<@'):
                    discordId = username[2:]
                    discordId = discordId.replace('>','')
                    username = bdd[str(discordId)]['name']
                    steamId = bdd[str(discordId)]["steamId"]
                else :
                    for user in bdd:
                        if str.lower(bdd[user]['name']) == username :
                            discordId = user
                            steamId = bdd[user]["steamId"]
                print(username, discordId)
                with open("datahero.json", "r") as jsonFile:
                    hereos_data = json.load(jsonFile)
                tiret_pos1 = ms.find('-',len(command)+len(username)-1)
                hero_name_input = ms[tiret_pos1+1:]
                hero_name = str.lower(hero_name_input.replace(' ',''))
                h = -1
                finish = False
                while finish is False :
                    for i in range(len(hereos_data)):
                        h = h+1
                        name = -1
                        for n in range(len(hereos_data[h]["used_names"])):
                            name = name+1
                            if hereos_data[h]["used_names"][name] == hero_name:
                                heroid=hereos_data[h]["id"]
                                herolocalisedname = hereos_data[h]["localized_name"]
                                await postmatch.send("Checking {}'s stats with {}, please wait...".format(str.capitalize(username), hereos_data[h]["localized_name"]))
                                finish = True
                                break
                                #sortir de la boucle for i in range(len(hereos_data)) quand le résultat est correct
                            else :
                                pass
                        if i == len(hereos_data):
                            finish = True
                        if finish == True :
                            break
                opendota_stats = apiparser.opendota_hero_stats(steamId, heroid)
                stratz_stats = apiparser.stratz_hero_stats(steamId, heroid)
                await postmatch.send('His statistics with **{}** in **{}** games :\n {}   {}% win\n {} games played with ({}% win)\n {} games played against ({}% win)\n            __Records :__\n      Kills : {} (*{}*)\n      Deaths : {} (*{}*)\n      Assists : {} (*{}*)\n      GPM : {} (*{}*)\n      XPM : {} (*{}*)\n      Last-hits : {} (*{}*)\n\n His winning streak is {} and record is {}{}'.format(herolocalisedname, opendota_stats[1], opendota_stats[4], opendota_stats[3], opendota_stats[5], opendota_stats[7], opendota_stats[8], opendota_stats[10], stratz_stats[3], stratz_stats[4], stratz_stats[5], stratz_stats[6], stratz_stats[7], stratz_stats[8], stratz_stats[9], stratz_stats[10], stratz_stats[11], stratz_stats[12], stratz_stats[13], stratz_stats[14], stratz_stats[0], stratz_stats[1],stratz_stats[2]))
            except:
                await postmatch.send('Invalid command, please try again : !command')
        else:
            f=0
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
            await access_logs.send('```diff\n+ {} IN  {}\n```'.format(utilitary.get_time(), name))
        elif after_channel == None and not before_channel == None:
            await access_logs.send('```diff\n- {} OUT {}\n```'.format(utilitary.get_time(), name))
    except Exception as e:
        print('Error in on_voice_state_update: {}'.format(e))

if __name__ == "__main__":
    try:
        client.run(token)
    except Exception as e:
        print('Error in __main__: {}'.format(e))
