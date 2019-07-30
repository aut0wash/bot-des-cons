import requests
import discord
import os
import asyncio
import time
import datetime
import pytz  # pip
import sys
import json

import setup as setup
import utilitary as utilitary
import commands as commands

def stratz_matchup(heroid, hereos_data):
    url = 'https://api.stratz.com/api/v1/Hero/' + str(heroid) + '/matchUp'
    heromatchup = utilitary.JSONRequester(url)
    top1counter = heromatchup["disadvantage"][0]["vs"][0]["heroId2"]
    h = -1
    for i in range(len(hereos_data)):
        h = h+1
        if hereos_data[h]["id"]==top1counter:
            top1counter_name = hereos_data[h]["localized_name"]
    top2counter = heromatchup["disadvantage"][0]["vs"][1]["heroId2"]
    h = -1
    for i in range(len(hereos_data)):
        h = h+1
        if hereos_data[h]["id"]==top2counter:
            top2counter_name = hereos_data[h]["localized_name"]
    top3counter = heromatchup["disadvantage"][0]["vs"][2]["heroId2"]
    h = -1
    for i in range(len(hereos_data)):
        h = h+1
        if hereos_data[h]["id"]==top3counter:
            top3counter_name = hereos_data[h]["localized_name"]
    top4counter = heromatchup["disadvantage"][0]["vs"][3]["heroId2"]
    h = -1
    for i in range(len(hereos_data)):
        h = h+1
        if hereos_data[h]["id"]==top4counter:
            top4counter_name = hereos_data[h]["localized_name"]
    top5counter = heromatchup["disadvantage"][0]["vs"][4]["heroId2"]
    h = -1
    for i in range(len(hereos_data)):
        h = h+1
        if hereos_data[h]["id"]==top5counter:
            top5counter_name = hereos_data[h]["localized_name"]

    return(top1counter_name, top2counter_name, top3counter_name, top4counter_name, top5counter_name)

def opendota_hero_stats(steam_id, hero_id):
    url = 'https://api.opendota.com/api/players/' + str(steam_id) + '/heroes'
    print("Getting stats from url", url, "for", steam_id, "about ID", hero_id)
    opendotaplayersherostats = utilitary.JSONRequester(url)
    for hero in range(len(opendotaplayersherostats)) :
        if opendotaplayersherostats[hero]['hero_id'] == str(hero_id):
            lastgame = opendotaplayersherostats[hero]['last_played']
            gamescount = opendotaplayersherostats[hero]['games']
            winscount = opendotaplayersherostats[hero]['win']
            winrate = round(((winscount/gamescount) * 100),1)
            if winrate >= 55 :
                com_win =':quandmeme:'
            elif winrate >= 50 and winrate <55 :
                com_win =':thumbsup:'
            elif winrate < 50 and winrate >= 45 :
                com_win =':thumbsdown:'
            else :
                com_win =':malaise:'
            withgames = opendotaplayersherostats[hero]['with_games']
            winwith = opendotaplayersherostats[hero]['with_win']
            winratewith = round(((winwith/withgames) * 100),1)
            againstgames = opendotaplayersherostats[hero]['against_games']
            winagainst = opendotaplayersherostats[hero]['against_win']
            winrateagainst = round(((winagainst/againstgames) * 100),1)

    return(lastgame, gamescount, winscount, winrate, com_win, withgames, winwith, winratewith, againstgames, winagainst, winrateagainst)

def stratz_hero_stats(steam_id, hero_id):
    url = 'https://api.stratz.com/api/v1/Player/' + str(steam_id) + '/heroPerformance/' + str(hero_id)
    print("Getting stats from url", url, "for", steam_id, "about ID", hero_id)
    stratzplayersherostats = utilitary.JSONRequester(url)
    currentstreak = stratzplayersherostats['streak']
    maxstreak = stratzplayersherostats['maxStreak']
    if currentstreak == maxstreak :
        com_streak = ' : :PogChamp:'
    elif maxstreak - currentstreak <=2 and maxstreak > 5:
        com_streak = " : you're not so far !"
    elif currentstreak ==1:
        com_streak = " : it's still better than a lose..."
    elif currentstreak ==0:
        com_streak = " : well, you should change hero..."
    else :
        com_streak = "!"
    avgkills =round(stratzplayersherostats['avgNumKills'],1)
    maxkills = stratzplayersherostats['maxNumKills']
    avgdeaths = round(stratzplayersherostats['avgNumDeaths'],1)
    mindeaths = stratzplayersherostats['maxNumDeaths']
    avgassists = round(stratzplayersherostats['avgNumAssists'],1)
    maxassists = stratzplayersherostats['maxNumAssists']
    avggpm = round(stratzplayersherostats['avgGoldPerMinute'])
    maxgpm = round(stratzplayersherostats['maxGoldPerMinute'])
    avgxpm = round(stratzplayersherostats['avgExperiencePerMinute'])
    maxxpm = round(stratzplayersherostats['maxExperiencePerMinute'])
    avglh = round(stratzplayersherostats['avgNumLastHits'])
    maxlh = stratzplayersherostats['maxNumLastHits']

    return(currentstreak, maxstreak, com_streak, avgkills, maxkills, avgdeaths, mindeaths, avgassists, maxassists, avggpm, maxgpm, avgxpm, maxxpm, avglh, maxlh)
