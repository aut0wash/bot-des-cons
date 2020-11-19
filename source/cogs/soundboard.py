import discord
from discord.ext import commands, tasks
import asyncio
import logging
import random
from pathlib import Path
import os.path
import json

import utils
from main import is_admin


class Soundboard(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.folder_root = Path().absolute()
        self.audio_folder = os.path.join(os.path.dirname(self.folder_root), "audios")
    @commands.command(aliases=['sound', 's'])
    @commands.dm_only()
    @commands.cooldown(3, 60, type=commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.guild, wait=True)
    async def soundboard(self, ctx, *sound_name):
        self.client.samples = utils.load_json("samples.json")
        sample_name = f"{' '.join(sound_name)}"
        logging.info(f"Command soundboard from {ctx.message.author.display_name}: {sample_name}")
        sample = None
        try:
            val = int(sample_name)
            sample = utils.get_sample_from_id(self.client.samples, val)
        except ValueError:
            sample = utils.get_sample_from_name(
                self.client.samples, sample_name)

        if sample:
            member = self.client.guild.get_member(ctx.message.author.id)
            connected = member.voice
            if connected:
                vc = await connected.channel.connect()
                vc.play(discord.FFmpegPCMAudio(f"{self.audio_folder}/{sample.path}", options=f"-vol {sample.volume}"), after=lambda e: logging.info(f"Finished, {e}"))

                while vc.is_playing():
                    await asyncio.sleep(0.5)
                await vc.disconnect()

    @commands.command(aliases=['rd', 'rand'])
    @commands.dm_only()
    @commands.cooldown(3, 60, type=commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.guild, wait=True)
    async def random(self, ctx):
        self.client.samples = utils.load_json("samples.json")
        logging.info(f"Command soundboard from {ctx.message.author.display_name}: random sound")
        sample = None

        random_id = random.randint(1,len(self.client.samples))
        val = int(random_id)
        sample = utils.get_sample_from_id(self.client.samples, val)

        if sample:
            member = self.client.guild.get_member(ctx.message.author.id)
            connected = member.voice
            if connected:
                vc = await connected.channel.connect()
                vc.play(discord.FFmpegPCMAudio(f"{self.audio_folder}/{sample.path}", options=f"-vol {sample.volume}"), after=lambda e: logging.info(f"Finished, {e}"))

                while vc.is_playing():
                    await asyncio.sleep(0.5)
                await vc.disconnect()

    @commands.command(aliases=['list', 'l'])
    @commands.dm_only()
    async def soundlist(self, ctx, tags=None):
        self.client.samples = utils.load_json("samples.json")
        logging.info(f"Command soundlist from {ctx.message.author.display_name}")
        command_list = []
        if tags is not None:
            samples_list = utils.get_sample_from_tags(self.client.samples, tags)
            for sample in samples_list:
                command_list.append(f"{sample}-{samples_list[sample]['path'].split('.')[0]}")

        else:

            for sample in self.client.samples:
                command_list.append(f"{sample}-{self.client.samples[sample]['path'].split('.')[0]}")

        await ctx.send("Voici la liste des sons disponibles:\n```css\n{}```".format('\n'.join(command_list)))

    @commands.command(aliases=['add_sound', 'add'])
    @is_admin()
    @commands.dm_only()
    async def addsound(self, ctx, tags=None):
        logging.info(f"Command addsound from {ctx.message.author.display_name}")
        new_sound = ctx.message.attachments[0]
        extension = os.path.splitext(new_sound.filename)[1]
        if extension == ".mp3":
            await new_sound.save(fp=os.path.join(os.path.dirname(self.folder_root), "audios", new_sound.filename))
            await ctx.send(f":white_check_mark: Fichier {new_sound.filename} ajouté dans la bibliothèque avec succès.")
        else:
            await ctx.send(f":negative_squared_cross_mark: Fichier {new_sound.filename} ne semble pas être dans le bon format (.mp3 uniquement).")

    @commands.command(aliases=['update', 'updatejson'])
    @is_admin()
    @commands.dm_only()
    async def update_bibliotheque(self, ctx, tags=None):
        logging.info(f"Command update_bibliotheque from {ctx.message.author.display_name}")
        new_samples_dict = ctx.message.attachments[0]

        if new_samples_dict.filename == "samples.json":
            await new_samples_dict.save(fp=os.path.join(os.path.dirname(self.folder_root), "audios", new_samples_dict.filename))
            await ctx.send(f":white_check_mark: {new_samples_dict.filename} mis à jour avec succès!")
            self.client.samples = utils.load_json("samples.json")

        else:
            await ctx.send(f":negative_squared_cross_mark: {new_sound.filename} ne semble pas correspondre (*samples.json* uniquement).")



def setup(client):
    client.add_cog(Soundboard(client))
