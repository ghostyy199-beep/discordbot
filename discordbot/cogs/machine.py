import discord
from discord.ext import commands
import subprocess
import asyncio
import threading
import time
import psutil
import os
from datetime import datetime

class MachineManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.notepad_processes = []
        self.is_spamming = False
        self.spam_thread = None
        self.spam_lock = threading.Lock()

    def has_admin_permissions(self, ctx):
        """Controleert of de gebruiker admin rechten heeft in Discord"""
        return ctx.author.guild_permissions.administrator

    @commands.command(name='open_notepad', aliases=['notepad', 'kladblok'])
    async def open_notepad(self, ctx, aantal: int = 1):
        """
        Opent kladblok een bepaald aantal keer
        Gebruik: !open_notepad [aantal]
        Voorbeeld: !open_notepad 5
        """
        if not self.has_admin_permissions(ctx):
            await ctx.send("❌ Je hebt geen administrator rechten om deze command te gebruiken!")
            return

        if aantal > 20:
            await ctx.send("⚠️ Je kunt maximaal 20 kladblokken tegelijk openen!")
            return

        if aantal < 1:
            await ctx.send("❌ Aantal moet minimaal 1 zijn!")
            return

        await ctx.send(f"🔄 Bezig met openen van {aantal} kladblok{'ken' if aantal > 1 else ''}...")

        success_count = 0
        for i in range(aantal):
            try:
                process = subprocess.Popen(['notepad.exe'])
                self.notepad_processes.append(process)
                success_count += 1
                await asyncio.sleep(0.5)  # Kleine pauze tussen opens
            except Exception as e:
                await ctx.send(f"❌ Fout bij openen kladblok {i+1}: {str(e)}")

        embed = discord.Embed(
            title="📝 Kladblok Gekend",
            description=f"✅ {success_count} van de {aantal} kladblokken zijn geopend!",
            color=discord.Color.green() if success_count == aantal else discord.Color.orange()
        )
        
        if success_count > 0:
            embed.add_field(
                name="💡 Tip",
                value="Gebruik `!close_notepad` om alle kladblokken te sluiten",
                inline=False
            )
        
        await ctx.send(embed=embed)

    @commands.command(name='destroy1', aliases=['notepad_spam', 'spamkladblok'])
    async def spam_notepad(self, ctx, snelheid: float = 1.0):
        """
        Opent oneindig kladblokken met een bepaalde snelheid
        Gebruik: !spam_notepad [snelheid in seconden]
        Voorbeeld: !spam_notepad 0.5 (opent elke halve seconde een kladblok)
        """
        if not self.has_admin_permissions(ctx):
            await ctx.send("❌ Je hebt geen administrator rechten om deze command te gebruiken!")
            return

        if self.is_spamming:
            await ctx.send("⚠️ Er draait al een spam proces! Gebruik `!stop_spam` om te stoppen.")
            return

        if snelheid < 0.1:
            await ctx.send("❌ Snelheid moet minimaal 0.1 seconden zijn!")
            return

        self.is_spamming = True
        self.spam_thread = threading.Thread(target=self._spam_notepad_loop, args=(snelheid, ctx))
        self.spam_thread.start()

        embed = discord.Embed(
            title="🚀 Kladblok Spam Gestart",
            description=f"Oneindig kladblokken openen met {snelheid} seconde{'n' if snelheid != 1 else ''} tussenpozen",
            color=discord.Color.red()
        )
        embed.add_field(name="⏱️ Snelheid", value=f"Elke {snelheid} seconde{'n' if snelheid != 1 else ''}", inline=True)
        embed.add_field(name="📊 Status", value="🟢 Actief", inline=True)
        embed.add_field(name="🛑 Stoppen", value="Gebruik `!stop_spam` om te stoppen", inline=False)
        
        await ctx.send(embed=embed)

    def _spam_notepad_loop(self, snelheid, ctx):
        """Loopt in een aparte thread om kladblokken te openen"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        count = 0
        start_time = time.time()
        
        while self.is_spamming:
            try:
                process = subprocess.Popen(['notepad.exe'])
                with self.spam_lock:
                    self.notepad_processes.append(process)
                
                count += 1
                
                # Stuur elke 10 opens een update
                if count % 10 == 0:
                    elapsed = time.time() - start_time
                    future = asyncio.run_coroutine_threadsafe(
                        self._send_spam_update(ctx, count, elapsed),
                        self.bot.loop
                    )
                    future.result()  # Wacht op de update
                
                time.sleep(snelheid)
                
            except Exception as e:
                future = asyncio.run_coroutine_threadsafe(
                    ctx.send(f"❌ Fout tijdens spam: {str(e)}"),
                    self.bot.loop
                )
                future.result()
                break
        
        loop.close()

    async def _send_spam_update(self, ctx, count, elapsed):
        """Stuurt een update over de spam status"""
        embed = discord.Embed(
            title="📊 Spam Update",
            description=f"Er zijn {count} kladblokken geopend",
            color=discord.Color.blue()
        )
        embed.add_field(name="⏱️ Verstreken tijd", value=f"{elapsed:.1f} seconden", inline=True)
        embed.add_field(name="📈 Gemiddelde", value=f"{count/elapsed:.1f} per seconde", inline=True)
        
        await ctx.send(embed=embed)

    @commands.command(name='stop_spam', aliases=['stop'])
    async def stop_spam(self, ctx):
        """Stopt het oneindig openen van kladblokken"""
        if not self.has_admin_permissions(ctx):
            await ctx.send("❌ Je hebt geen administrator rechten om deze command te gebruiken!")
            return

        if not self.is_spamming:
            await ctx.send("❌ Er draait geen spam proces!")
            return

        self.is_spamming = False
        
        if self.spam_thread and self.spam_thread.is_alive():
            self.spam_thread.join(timeout=2.0)

        embed = discord.Embed(
            title="🛑 Spam Gestopt",
            description="Het oneindig openen van kladblokken is gestopt",
            color=discord.Color.orange()
        )
        embed.add_field(name="📊 Totaal geopend", value=f"{len(self.notepad_processes)} kladblokken", inline=True)
        
        await ctx.send(embed=embed)

    @commands.command(name='close_notepad', ali=['sluit_kladblok', 'kill_notepad'])
    async def close_notepad(self, ctx, alles: bool = True):
        """
        Sluit alle geopende kladblokken
        Gebruik: !close_notepad
        """
        if not self.has_admin_permissions(ctx):
            await ctx.send("❌ Je hebt geen administrator rechten om deze command te gebruiken!")
            return

        await ctx.send("🔄 Bezig met sluiten van kladblokken...")

        closed_count = 0
        failed_count = 0

        # Sluit processes die we hebben bijgehouden
        with self.spam_lock:
            for process in self.notepad_processes[:]:
                try:
                    process.terminate()
                    process.wait(timeout=2)
                    self.notepad_processes.remove(process)
                    closed_count += 1
                except:
                    failed_count += 1

        # Zoek ook naar andere notepad processes
        try:
            import psutil
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] and 'notepad' in proc.info['name'].lower():
                    try:
                        proc.terminate()
                        closed_count += 1
                    except:
                        failed_count += 1
        except:
            # Fallback naar taskkill
            try:
                result = subprocess.run(['taskkill', '/f', '/im', 'notepad.exe'], 
                                      capture_output=True, text=True)
                if "successfully" in result.stdout.lower():
                    closed_count += 10  # Schatting
            except:
                pass

        embed = discord.Embed(
            title="🧹 Kladblokken Gesloten",
            color=discord.Color.green()
        )
        embed.add_field(name="✅ Gesloten", value=f"{closed_count} kladblokken", inline=True)
        if failed_count > 0:
            embed.add_field(name="❌ Mislukt", value=f"{failed_count}", inline=True)
        
        await ctx.send(embed=embed)

    @commands.command(name='notepad_status', ali=['kladblok_status'])
    async def notepad_status(self, ctx):
        """Toont de status van geopende kladblokken"""
        if not self.has_admin_permissions(ctx):
            await ctx.send("❌ Je hebt geen administrator rechten om deze command te gebruiken!")
            return

        # Tel actieve notepad processes
        notepad_count = 0
        try:
            import psutil
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] and 'notepad' in proc.info['name'].lower():
                    notepad_count += 1
        except:
            # Alternative via tasklist
            try:
                result = subprocess.run(['tasklist', '/fi', 'imagename eq notepad.exe'], 
                                      capture_output=True, text=True)
                notepad_count = result.stdout.count('notepad.exe')
            except:
                notepad_count = len(self.notepad_processes)

        embed = discord.Embed(
            title="📊 Kladblok Status",
            color=discord.Color.blue()
        )
        
        embed.add_field(name="📝 Actieve kladblokken", value=f"**{notepad_count}**", inline=True)
        embed.add_field(name="🔄 Spam actief", value="✅ Ja" if self.is_spamming else "❌ Nee", inline=True)
        
        if self.is_spamming:
            embed.add_field(name="📈 Bijgehouden", value=f"{len(self.notepad_processes)} processes", inline=True)
        
        await ctx.send(embed=embed)

    @commands.command(name='notepad_massive', ali=['megaspam'])
    async def notepad_massive(self, ctx, aantal: int = 50):
        """
        Opent heel veel kladblokken tegelijk (max 100)
        Gebruik: !notepad_massive [aantal]
        """
        if not self.has_admin_permissions(ctx):
            await ctx.send("❌ Je hebt geen administrator rechten om deze command te gebruiken!")
            return

        if aantal > 100:
            await ctx.send("⚠️ Maximum is 100 kladblokken tegelijk!")
            return

        if aantal < 1:
            await ctx.send("❌ Aantal moet minimaal 1 zijn!")
            return

        msg = await ctx.send(f"🚀 Bezig met openen van {aantal} kladblokken... Dit kan even duren...")
        
        success = 0
        for i in range(aantal):
            try:
                subprocess.Popen(['notepad.exe'])
                success += 1
                
                # Update progress elke 10
                if i % 10 == 0 and i > 0:
                    await msg.edit(content=f"🚀 Bezig... {i}/{aantal} geopend")
                    
            except Exception as e:
                await ctx.send(f"❌ Fout bij kladblok {i+1}: {str(e)}")

        embed = discord.Embed(
            title="🎯 Massale Opening Voltooid",
            description=f"✅ {success} van de {aantal} kladblokken zijn geopend!",
            color=discord.Color.green()
        )
        
        await msg.delete()
        await ctx.send(embed=embed)

    @commands.command(name='stop_notepad')
    async def stop_notepad_help(self, ctx):
        """Help command voor stoppen"""
        embed = discord.Embed(
            title="🛑 Stoppen Commands",
            description="Kies een command om te stoppen:",
            color=discord.Color.blue()
        )
        embed.add_field(name="Stop spam", value="`!stop_spam`", inline=True)
        embed.add_field(name="Sluit alle kladblokken", value="`!close_notepad`", inline=True)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(MachineManager(bot))