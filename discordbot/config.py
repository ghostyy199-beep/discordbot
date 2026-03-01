import discord

TOKEN = ""

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

STARTUP_CHANNEL_ID = 1468946622321791050  # vervang dit met je channel ID
BANNER_PATH = "banner.png"              # pad naar je banner