from discord.ext import commands
from services.windowsdef import WindowsDefender


class Defender(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

## Deze cog bevat commando's om de status van Windows Defender realtime protection te controleren en uit te schakelen.

    @commands.command(help="Checkt de status van Windows Defender realtime protection.")
    async def defender_status(self, ctx):
        try:
            status = WindowsDefender.is_realtime_enabled()

            if status:
                await ctx.send("Realtime protection staat AAN")
            else:
                await ctx.send("Realtime protection staat UIT")

        except Exception as e:
            await ctx.send(f"Fout: {e}")

## Deze commando schakelt Windows Defender realtime protection uit. Alleen de eigenaar van de bot kan dit commando gebruiken.

    @commands.command(help="Schakelt Windows Defender realtime protection uit.")
    @commands.is_owner()
    async def defender_disable(self, ctx):
        try:
            WindowsDefender.disable_realtime()
            await ctx.send("Realtime protection uitgeschakeld")

        except Exception as e:
            await ctx.send(f"Fout: {e}")


async def setup(bot):
    await bot.add_cog(Defender(bot))