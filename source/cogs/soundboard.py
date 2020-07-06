import discord
from discord.ext import commands, tasks
import asyncio
import logging

import utils
from main import is_admin



class Soundboard(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['sound', 's'])
    @is_admin()
    @commands.dm_only()
    @commands.cooldown(3, 60, type= commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.guild, wait=True)
    async def soundboard(self, ctx, sample_name : str):
        logging.info(f'Command from {ctx.message.author.display_name}: {sample_name}')

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



def setup(client):
    client.add_cog(Soundboard(client))
