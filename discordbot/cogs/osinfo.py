import discord
from discord.ext import commands
import platform
import psutil
import socket

##Haalt OS en systeeminformatie op. Volledig los van Discord zodat het herbruikbaar is.

def get_system_info() -> dict:

    return {
        "os": platform.system(),
        "os_release": platform.release(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "hostname": socket.gethostname(),
        "cpu": platform.processor(),
        "cpu_cores": psutil.cpu_count(logical=True),
        "ram_total": round(psutil.virtual_memory().total / (1024**3), 2),
    }


class OSInfo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="osinfo", help="Toont informatie over het besturingssysteem en hardware.")
    async def os_info(self, ctx: commands.Context):
        info = get_system_info()

        embed = discord.Embed(
            title="💻 Systeem Informatie",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="Besturingssysteem",
            value=f"{info['os']} {info['os_release']}",
            inline=False
        )
        embed.add_field(name="Versie", value=info['os_version'], inline=False)
        embed.add_field(name="Architectuur", value=info['architecture'], inline=True)
        embed.add_field(name="CPU", value=info['cpu'], inline=False)
        embed.add_field(name="CPU Cores", value=info['cpu_cores'], inline=True)
        embed.add_field(name="RAM (GB)", value=f"{info['ram_total']} GB", inline=True)
        embed.add_field(name="Hostname", value=info['hostname'], inline=False)

        embed.set_footer(text="NAWIDS BOT • Systeem Info")

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(OSInfo(bot))