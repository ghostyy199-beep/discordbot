from discord.ext import commands
from discord import Embed

## Deze cog bevat basiscommando's zoals ping en help.
class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ## Ping commando
    @commands.command(help="Checkt of de bot online is.")
    async def ping(self, ctx):
        await ctx.send("Pong!")

## Help commando met simpele tekstweergave (geen embed)
    @commands.command(name="help", help="Laat alle commando's zien.")
    async def help_command(self, ctx):
        # Stuur eerst een header
        await ctx.send("**📚 Beschikbare commando's:**")
        await ctx.send("Hier is een lijst van alle commando's die je kunt gebruiken:")
        await ctx.send("─" * 40)

        # Sorteer commando's alfabetisch
        sorted_commands = sorted(self.bot.commands, key=lambda cmd: cmd.name.lower())

        # Bouw de berichten in stukken (Discord heeft een limiet van 2000 karakters per bericht)
        current_message = ""
        
        for cmd in sorted_commands:
            if not cmd.hidden:
                command_text = f"**!{cmd.name}** - {cmd.help}\n"
                
                # Als het huidige bericht + nieuwe command te lang wordt, stuur het huidige bericht
                if len(current_message) + len(command_text) > 1900:  # Iets onder de 2000 limiet
                    await ctx.send(current_message)
                    current_message = command_text
                else:
                    current_message += command_text

        # Stuur het laatste bericht als er nog iets over is
        if current_message:
            await ctx.send(current_message)

        # Stuur een footer
        await ctx.send("─" * 40)
        await ctx.send("Gebruik **!help [commando]** voor meer info over een specifiek commando.")

# Async setup functie die de cog registreert
async def setup(bot):
    await bot.add_cog(Basic(bot))