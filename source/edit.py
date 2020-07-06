from discord.ext import commands, tasks, cooldown, BucketType

bot = commands.Bot(command_prefix='!', description=description)


def is_admin():
    def predicate(ctx):
        return ctx.message.author.id in authorized_ids
    return commands.check(predicate)



if __name__ == "__main__":
    try:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                bot.load_extension(f'cogs.{filename[:-3]}')
        # bot.get_cog(name) x3
        """for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                bot.load_extension(f'cogs.{filename[:-3]}')"""
        bot.run(TOKEN)

    except Exception as e:
        print(e)


### cogs/soundboard.py
from main import is_admin


class Soundboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['soundboard', 'sound', 's'])
    @is_admin()
    @commands.dm_only()
    @commands.cooldown(3, 60, type= BucketType.user)
    @commands.max_concurrency(1, per=BucketType.guild, *, wait=True)
    async def soundboard(self, ctx, sample_name : str):
    
      sample = utils.get_sample_from_name(
                client.samples, sample_name)
                
            if sample:
                member = client.guild.get_member(ctx.author.id)
                connected = member.voice
                if connected:
                    vc = await connected.channel.connect()
                    vc.play(discord.FFmpegPCMAudio(f"/root/discord/{sample.path}", options=f"-vol {sample.volume}"), after=lambda e: logging.info(f"Finished, {e}"))

                    while vc.is_playing():
                        await asyncio.sleep(0.5)
                    await vc.disconnect()
