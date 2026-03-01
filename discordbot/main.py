import discord
from discord.ext import commands
from config import BANNER_PATH, STARTUP_CHANNEL_ID, TOKEN, intents
from utils.banner import print_banner


class NawidsBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        # Cogs laden
        await self.load_extension("cogs.basic")
        await self.load_extension("cogs.media")
        await self.load_extension("cogs.activity")
        await self.load_extension("cogs.defender")
        await self.load_extension("cogs.osinfo")
        await self.load_extension("cogs.user")
        await self.load_extension("cogs.machine")
        await self.load_extension("cogs.machine2")

## Discord Banner Code

    async def on_ready(self):
        print_banner()
        print(f"Bot is online als {self.user}")

        channel = self.get_channel(STARTUP_CHANNEL_ID)
        if channel is None:
            print("Kanaal niet gevonden")
            return

        embed = discord.Embed(
            title="Bot opgestart",
            description="**De bot is succesvol opgestart en klaar voor gebruik!**",
            color=discord.Color.green()
        )

        embed.set_footer(text="NAWIDS BOT • Online")

        try:
            file = discord.File(BANNER_PATH, filename="banner.png")
            embed.set_image(url="attachment://banner.png")
            await channel.send(embed=embed, file=file)
        except Exception as e:
            print(f"Fout bij verzenden banner: {e}")

bot = NawidsBot()
bot.run(TOKEN)