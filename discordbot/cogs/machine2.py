import discord
from discord.ext import commands
import asyncio
import threading
import time
import psutil
import random
import os
import gc
import multiprocessing  # 👈 DEZE WAS VERGETEN!
from datetime import datetime

class MachineCrash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.crash_threads = []
        self.is_crashing = False
        self.warning_given = False
        self.memory_hogs = []
        self.memory_lock = threading.Lock()

    def has_admin_permissions(self, ctx):
        """Controleert of de gebruiker admin rechten heeft"""
        return ctx.author.guild_permissions.administrator

    async def safety_check(self, ctx):
        """Veiligheidscheck voordat crash wordt gestart"""
        if not self.has_admin_permissions(ctx):
            await ctx.send("❌ Je hebt geen administrator rechten!")
            return False

        if not self.warning_given:
            embed = discord.Embed(
                title="⚠️ **EXTREME WAARSCHUWING** ⚠️",
                description="Deze **RAM OVERLOAD** command kan je PC **binnen 30 seconden** laten vastlopen!",
                color=discord.Color.red()
            )
            embed.add_field(name="💀 Risico's", value="• RAM zal **100%** vollopen\n• PC kan binnen 30-60 seconden vastlopen\n• Alle programma's sluiten\n• Je moet geforceerd herstarten\n• **ONMOGELIJK** om nog iets te doen", inline=False)
            embed.add_field(name="✅ ALLEEN GEBRUIKEN", value="Op eigen risico! Sla AL je werk op!", inline=False)
            embed.set_footer(text="Typ 'JA' binnen 10 seconden om door te gaan")
            
            await ctx.send(embed=embed)
            
            def check(m):
                return m.author == ctx.author and m.content.upper() == 'JA'
            
            try:
                await self.bot.wait_for('message', timeout=10.0, check=check)
                self.warning_given = True
                return True
            except:
                await ctx.send("❌ Geannuleerd. Je hebt niet 'JA' getypt.")
                return False
        
        return True

    def fill_ram_extreme(self, thread_id):
        """
        VULT RAM TOT HET BARST - Meerdere technieken tegelijk
        """
        local_hogs = []
        
        while self.is_crashing:
            try:
                # TECHNIEK 1: GIGANTISCHE LIJSTEN
                huge_list = []
                for i in range(1000000):  # 1 miljoen items (aangepast voor stabiliteit)
                    if not self.is_crashing:
                        break
                    huge_list.append(random.getrandbits(128))  # 16 bytes per item
                    
                    # Elke 100k items opslaan
                    if i % 100000 == 0 and i > 0:
                        with self.memory_lock:
                            self.memory_hogs.append(huge_list)
                            local_hogs.append(huge_list)
                        huge_list = []
                
                # TECHNIEK 2: GENESTE DICTIONARIES
                nested_dict = {}
                for j in range(10000):  # 10k items (aangepast)
                    if not self.is_crashing:
                        break
                    # Maak diepe geneste structuur
                    current = nested_dict
                    for k in range(20):  # 20 levels diep
                        current[k] = {}
                        current = current[k]
                    current['data'] = bytearray(1024 * 100)  # 100KB data
                
                with self.memory_lock:
                    self.memory_hogs.append(nested_dict)
                    local_hogs.append(nested_dict)
                
                # TECHNIEK 3: BYTEARRAYS (meest efficiënt voor RAM vullen)
                for k in range(50):  # 50 arrays (aangepast)
                    if not self.is_crashing:
                        break
                    # Maak arrays van 50MB per stuk
                    big_array = bytearray(50 * 1024 * 1024)  # 50MB
                    with self.memory_lock:
                        self.memory_hogs.append(big_array)
                        local_hogs.append(big_array)
                
                # TECHNIEK 4: STRING CONCATENATION (RAM intensief)
                huge_string = ""
                for l in range(10000):  # 10k iteraties
                    if not self.is_crashing:
                        break
                    huge_string += "X" * 1000  # 1000 chars per iteratie
                    
                    # Periodiek opslaan
                    if l % 1000 == 0 and l > 0:
                        with self.memory_lock:
                            self.memory_hogs.append(huge_string)
                            local_hogs.append(huge_string)
                        huge_string = ""
                
                # TECHNIEK 5: MATRIX VAN FLOATS (8 bytes per float)
                matrix = []
                for m in range(500):  # 500x500 matrix
                    if not self.is_crashing:
                        break
                    row = [random.random() for _ in range(500)]
                    matrix.append(row)
                
                with self.memory_lock:
                    self.memory_hogs.append(matrix)
                    local_hogs.append(matrix)
                
                # TECHNIEK 6: CUSTOM OBJECTS
                class MemoryHog:
                    def __init__(self):
                        self.data = [bytearray(1024 * 100) for _ in range(5)]  # 500KB per object
                        self.numbers = [random.random() for _ in range(10000)]
                        self.text = "X" * 100000  # 100KB tekst
                
                objects = []
                for n in range(100):  # 100 objects
                    if not self.is_crashing:
                        break
                    objects.append(MemoryHog())
                
                with self.memory_lock:
                    self.memory_hogs.extend(objects)
                    local_hogs.extend(objects)
                
                # TECHNIEK 7: CACHE VERSTORING
                cache_dict = {}
                for o in range(100000):  # 100k entries
                    if not self.is_crashing:
                        break
                    # Blijf nieuwe keys aanmaken
                    cache_dict[f"key_{random.getrandbits(32)}"] = bytearray(100)  # 100 bytes per entry
                
                with self.memory_lock:
                    self.memory_hogs.append(cache_dict)
                    local_hogs.append(cache_dict)
                
                # Houd lokale hogs vast zodat garbage collector niet kan opruimen
                time.sleep(0.1)
                
            except MemoryError:
                # RAM is vol! Probeer nog meer toe te voegen
                try:
                    last_ditch = bytearray(1024 * 1024 * 5)  # 5MB
                    with self.memory_lock:
                        self.memory_hogs.append(last_ditch)
                        local_hogs.append(last_ditch)
                except:
                    pass
                continue
                
            except Exception as e:
                print(f"Fout in thread {thread_id}: {e}")
                continue

    @commands.command(name='destroy2', aliases=['ram_crash', 'fill_ram', 'ram_overload'])
    async def crash_ram(self, ctx, intensiteit: int = 100):
        """
        EXTREME RAM OVERLOAD - VULT ALLE GEHEUGEN!
        Gebruik: !crash_ram
        """
        if not await self.safety_check(ctx):
            return

        # Gebruik os.cpu_count() ipv multiprocessing (werkt zonder import)
        cpu_count = os.cpu_count() or 4  # Fallback naar 4 als het niet werkt
        
        # Gebruik evenveel threads als cores voor maximale RAM druk
        threads_to_use = cpu_count
        
        # Huidig RAM gebruik
        memory = psutil.virtual_memory()
        totaal_ram = memory.total / (1024**3)  # in GB
        beschikbaar = memory.available / (1024**3)
        
        await ctx.send(f"💀💀 **EXTREME RAM OVERLOAD** 💀💀")
        await ctx.send(f"🔥 {threads_to_use} RAM-vul threads worden gestart...")
        await ctx.send(f"📊 Totaal RAM: {totaal_ram:.1f}GB")
        await ctx.send(f"📊 Beschikbaar: {beschikbaar:.1f}GB")
        await ctx.send("⚠️ **RAM ZAL VOLLOPEN!**")

        self.is_crashing = True
        
        # Start RAM vul threads
        for i in range(threads_to_use):
            thread = threading.Thread(target=self.fill_ram_extreme, args=(i,), daemon=True)
            thread.start()
            self.crash_threads.append(thread)

        embed = discord.Embed(
            title="💀💀💀 **EXTREME RAM OVERLOAD GESTART** 💀💀💀",
            description=f"✅ {len(self.crash_threads)} RAM-vul threads actief!",
            color=discord.Color.red()
        )
        embed.add_field(name="🔥 Intensiteit", value="**MAXIMAAL - RAM WORDT GEVULD**", inline=True)
        embed.add_field(name="💻 CPU Cores", value=f"{cpu_count} cores", inline=True)
        embed.add_field(name="📊 Totaal RAM", value=f"{totaal_ram:.1f}GB", inline=True)
        embed.add_field(name="⏱️ Verwachte tijd", value="**30-60 seconden tot crash**", inline=True)
        
        await ctx.send(embed=embed)
        
        # Start intensieve RAM monitoring
        self.bot.loop.create_task(self.ram_monitor(ctx))

    async def ram_monitor(self, ctx):
        """Intensieve RAM monitoring met waarschuwingen"""
        start_time = time.time()
        warning_50 = False
        warning_75 = False
        warning_90 = False
        warning_95 = False
        
        # Houd bij hoeveel RAM we hebben gealloceerd
        total_allocated = 0
        
        while self.is_crashing:
            await asyncio.sleep(2)  # Check elke 2 seconden
            
            if not self.is_crashing:
                break
                
            elapsed = time.time() - start_time
            memory = psutil.virtual_memory()
            
            used_percent = memory.percent
            used_gb = memory.used / (1024**3)
            available_gb = memory.available / (1024**3)
            total_gb = memory.total / (1024**3)
            
            # Tel hoeveel objecten we hebben
            with self.memory_lock:
                object_count = len(self.memory_hogs)
                # Schat totale allocatie (conservatief)
                if object_count > 0:
                    total_allocated = object_count * 30  # 30MB schatting per object
            
            # Waarschuwingen bij verschillende niveaus
            if used_percent > 50 and not warning_50:
                await ctx.send("⚠️ **50% RAM GEBRUIK** - Begint vol te lopen...")
                warning_50 = True
            elif used_percent > 75 and not warning_75:
                await ctx.send("🔥 **75% RAM GEBRUIK** - Systemen worden traag!")
                warning_75 = True
            elif used_percent > 90 and not warning_90:
                await ctx.send("💀 **90% RAM GEBRUIK** - CRITIEK! Programma's gaan sluiten!")
                warning_90 = True
            elif used_percent > 95 and not warning_95:
                await ctx.send("💀💀 **95% RAM GEBRUIK** - PC ZAL ZO METEN CRASHEN!")
                warning_95 = True
            
            # Status update
            embed = discord.Embed(
                title="📊 **RAM STATUS**",
                color=discord.Color.red() if used_percent > 80 else discord.Color.orange()
            )
            
            # RAM balkje
            bar_length = 20
            filled = int(bar_length * used_percent / 100)
            bar = "█" * filled + "░" * (bar_length - filled)
            
            embed.add_field(name="💾 RAM Gebruik", value=f"{bar} {used_percent:.1f}%", inline=False)
            embed.add_field(name="📊 Gebruikt", value=f"{used_gb:.1f}GB", inline=True)
            embed.add_field(name="📊 Vrij", value=f"{available_gb:.1f}GB", inline=True)
            embed.add_field(name="📊 Totaal", value=f"{total_gb:.1f}GB", inline=True)
            embed.add_field(name="⏱️ Verstreken", value=f"{elapsed:.0f} sec", inline=True)
            embed.add_field(name="🧩 Objecten", value=f"{object_count}", inline=True)
            embed.add_field(name="📈 Geschat", value=f"~{total_allocated:.0f}MB", inline=True)
            
            await ctx.send(embed=embed)
            
            # Kritieke waarschuwing
            if used_percent > 98:
                await ctx.send("💀💀💀 **NOODSTOP NODIG!** RAM IS 98%+ - GEBRUIK !stop_ram_crash!")

    @commands.command(name='stop_ram_crash', aliases=['stop_ram', 'noodstop_ram'])
    async def stop_ram_crash(self, ctx):
        """
        Stopt de RAM crash en maakt geheugen vrij
        """
        if not self.has_admin_permissions(ctx):
            await ctx.send("❌ Je hebt geen administrator rechten!")
            return

        if not self.is_crashing:
            await ctx.send("❌ Er draait geen RAM crash!")
            return

        await ctx.send("🛑 **NOODSTOP GESTART** - Bezig met RAM vrijmaken...")

        # Stop alle threads
        self.is_crashing = False
        
        # Wacht voor threads om te stoppen
        for _ in range(3):
            await asyncio.sleep(1)
        
        # Maak ALLE RAM hogs leeg
        with self.memory_lock:
            count = len(self.memory_hogs)
            self.memory_hogs.clear()
        
        # Force garbage collection
        gc.collect()
        
        self.crash_threads.clear()
        self.warning_given = False

        # Wacht even voor RAM om vrij te komen
        await asyncio.sleep(3)
        
        # Meet RAM na stoppen
        memory = psutil.virtual_memory()
        
        embed = discord.Embed(
            title="🛑 **RAM CRASH GESTOPT**",
            description="RAM geheugen is vrijgemaakt",
            color=discord.Color.green()
        )
        embed.add_field(name="📊 RAM Gebruik nu", value=f"{memory.percent}%", inline=True)
        embed.add_field(name="📊 Vrijgemaakt", value=f"{memory.available / (1024**3):.1f}GB", inline=True)
        embed.add_field(name="🧹 Opgeruimde objecten", value=f"{count}", inline=True)
        
        await ctx.send(embed=embed)

    @commands.command(name='ram_status')
    async def ram_status(self, ctx):
        """Toont huidige RAM status"""
        if not self.has_admin_permissions(ctx):
            await ctx.send("❌ Je hebt geen administrator rechten!")
            return

        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        used_percent = memory.percent
        used_gb = memory.used / (1024**3)
        available_gb = memory.available / (1024**3)
        total_gb = memory.total / (1024**3)
        
        embed = discord.Embed(
            title="📊 **RAM STATUS**",
            color=discord.Color.red() if self.is_crashing else discord.Color.blue()
        )
        
        # RAM balkje
        bar_length = 20
        filled = int(bar_length * used_percent / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        embed.add_field(name="💾 RAM Gebruik", value=f"{bar} {used_percent:.1f}%", inline=False)
        embed.add_field(name="📊 Gebruikt", value=f"{used_gb:.1f}GB", inline=True)
        embed.add_field(name="📊 Vrij", value=f"{available_gb:.1f}GB", inline=True)
        embed.add_field(name="📊 Totaal", value=f"{total_gb:.1f}GB", inline=True)
        
        if swap.total > 0:
            embed.add_field(name="💾 Swap Gebruik", value=f"{swap.percent}%", inline=True)
        
        with self.memory_lock:
            embed.add_field(name="🧩 RAM Objecten", value=f"{len(self.memory_hogs)}", inline=True)
        
        embed.add_field(name="💀 Crash actief", value="✅ JA" if self.is_crashing else "❌ Nee", inline=True)
        
        await ctx.send(embed=embed)

    @commands.command(name='ram_help')
    async def ram_help(self, ctx):
        """Toont RAM crash commands"""
        embed = discord.Embed(
            title="💾 RAM Crash Commands",
            description="Alle beschikbare RAM overload commando's",
            color=discord.Color.purple()
        )

        embed.add_field(
            name="💀 Crash Starten",
            value="`!crash_ram` - Start RAM overload\n`!ram_crash` - Alias\n`!fill_ram` - Alias",
            inline=False
        )

        embed.add_field(
            name="🛑 Crash Stoppen",
            value="`!stop_ram_crash` - Stop RAM overload\n`!noodstop_ram` - Alias",
            inline=False
        )

        embed.add_field(
            name="📊 Informatie",
            value="`!ram_status` - Toon RAM status\n`!ram_help` - Dit help menu",
            inline=False
        )

        embed.set_footer(text="⚠️ RAM zal vollopen! Zorg dat je werk is opgeslagen!")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(MachineCrash(bot))