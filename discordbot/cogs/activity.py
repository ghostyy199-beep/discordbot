from discord.ext import commands
import discord
import datetime

## Deze cog houdt de activiteit van gebruikers bij en logt statusveranderingen in de console.

class Activity(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_message_activity = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            self.last_message_activity[message.author.id] = datetime.datetime.utcnow()

## Logt de statusverandering van gebruikers in de console
    @commands.Cog.listener()
    async def on_presence_update(self, before, after):
        if before.status != after.status:
            print(f"{after.name}: {before.status} → {after.status}")

## Bekijkt de laatste activiteit van een gebruiker of zichzelf als er geen gebruiker is opgegeven

    @commands.command(help="Bekijkt laatste activiteit.")
    async def activity(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        last = self.last_message_activity.get(member.id)

        if not last:
            await ctx.send("Geen activiteit geregistreerd.")
        else:
            await ctx.send(
                f"Laatste bericht van **{member.display_name}**:\n{last} UTC"
            )

## Toont inactieve gebruikers op basis van de laatste activiteit

    @commands.command(help="Toont inactieve gebruikers.")
    async def inactive(self, ctx, minutes: int = 10):
        now = datetime.datetime.utcnow()
        inactive = [
            f"<@{uid}>"
            for uid, last in self.last_message_activity.items()
            if (now - last).total_seconds() > minutes * 60
        ]

        if not inactive:
            await ctx.send("Iedereen is actief.")
        else:
            await ctx.send(
                f"Inactieve gebruikers ({minutes} min):\n" + ", ".join(inactive)
            )

async def setup(bot):
    await bot.add_cog(Activity(bot))