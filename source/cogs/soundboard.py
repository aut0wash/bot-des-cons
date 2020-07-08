import discord
from discord.ext import commands, tasks
import asyncio
import logging
import random
import utils
from main import is_admin


class Soundboard(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['sound', 's'])
    @is_admin()
    @commands.dm_only()
    @commands.cooldown(3, 60, type=commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.guild, wait=True)
    async def soundboard(self, ctx, *sound_name):
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
                vc.play(discord.FFmpegPCMAudio(f"/root/discord/{sample.path}", options=f"-vol {sample.volume}"), after=lambda e: logging.info(f"Finished, {e}"))

                while vc.is_playing():
                    await asyncio.sleep(0.5)
                await vc.disconnect()

    @commands.command(aliases=['rd', 'rand'])
    @is_admin()
    @commands.dm_only()
    @commands.cooldown(3, 60, type=commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.guild, wait=True)
    async def random(self, ctx):
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
                vc.play(discord.FFmpegPCMAudio(f"/root/discord/{sample.path}", options=f"-vol {sample.volume}"), after=lambda e: logging.info(f"Finished, {e}"))

                while vc.is_playing():
                    await asyncio.sleep(0.5)
                await vc.disconnect()

    @commands.command(aliases=['list', 'l'])
    @commands.dm_only()
    async def soundlist(self, ctx, tags=None):
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


def setup(client):
    client.add_cog(Soundboard(client))
