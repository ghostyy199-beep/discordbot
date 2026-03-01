import discord
from discord.ext import commands
import subprocess
import random
import string
import ctypes
import re
from datetime import datetime

class UserManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_admin_windows(self):
        """Controleert of de bot als administrator draait"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def generate_random_password(self, length=12):
        """Genereert een willekeurig wachtwoord"""
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.choice(characters) for i in range(length))
        return password

    async def check_permissions(self, ctx):
        """Controleert of de gebruiker de juiste rechten heeft"""
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("❌ Je hebt geen administrator rechten in Discord!")
            return False
        
        if not self.is_admin_windows():
            await ctx.send("⚠️ De bot moet als Windows Administrator draaien!")
            return False
        
        return True

    @commands.command(name='add_user', aliases=['newuser', 'createuser', 'adduser'])
    async def add_user(self, ctx, username: str, password: str = None):
        """
        Voegt een nieuwe Windows gebruiker toe
        Gebruik: !add_user <gebruikersnaam> [wachtwoord]
        """
        if not await self.check_permissions(ctx):
            return

        # Valideer gebruikersnaam
        if len(username) < 3 or len(username) > 20:
            await ctx.send("❌ Gebruikersnaam moet tussen 3 en 20 karakters zijn!")
            return

        if not re.match(r'^[a-zA-Z0-9._-]+$', username):
            await ctx.send("❌ Gebruikersnaam mag alleen letters, cijfers, punten, underscores en streepjes bevatten!")
            return

        # Als er geen wachtwoord is opgegeven, genereer er een
        if password is None:
            password = self.generate_random_password()
            auto_generated = True
        else:
            auto_generated = False
        
        # Stuur een "bezig" bericht
        status_msg = await ctx.send("🔄 Bezig met aanmaken van gebruiker...")
        
        try:
            # Eenvoudige PowerShell command zonder complexe error handling
            ps_command = f"""
            Write-Output "=== START ==="
            Write-Output "Proberen gebruiker {username} aan te maken..."
            
            try {{
                $password = ConvertTo-SecureString "{password}" -AsPlainText -Force
                New-LocalUser -Name "{username}" -Password $password -FullName "{username}" -ErrorAction Stop
                Write-Output "Gebruiker aangemaakt, nu toevoegen aan groep..."
                
                Add-LocalGroupMember -Group "Gebruikers" -Member "{username}" -ErrorAction Stop
                Write-Output "Toegevoegd aan groep Gebruikers"
                
                Write-Output "SUCCESS"
            }}
            catch {{
                Write-Output "ERROR: $($_.Exception.Message)"
                Write-Output "FAILED"
            }}
            Write-Output "=== EINDE ==="
            """
            
            # Voer PowerShell command uit
            result = subprocess.run(
                ["powershell.exe", "-Command", ps_command],
                capture_output=True,
                text=True,
                check=False
            )
            
            # DEBUG: Print ALLE output naar console
            print("\n" + "="*50)
            print("POWERSHELL OUTPUT:")
            print("="*50)
            print("STDOUT:")
            print(result.stdout)
            print("\nSTDERR:")
            print(result.stderr)
            print("="*50 + "\n")
            
            # Maak een debug embed met de output
            debug_embed = discord.Embed(
                title="🔧 Debug Informatie",
                description="PowerShell output wordt getoond in de console",
                color=discord.Color.orange()
            )
            
            # Kijk of we SUCCESS vinden in de output
            if "SUCCESS" in result.stdout:
                await status_msg.delete()
                
                embed = discord.Embed(
                    title="✅ Windows Gebruiker Aangemaakt",
                    description=f"Gebruiker **{username}** is succesvol toegevoegd",
                    color=discord.Color.green()
                )
                
                embed.add_field(name="📝 Gebruikersnaam", value=f"`{username}`", inline=True)
                
                if auto_generated:
                    embed.add_field(
                        name="🔑 Wachtwoord", 
                        value=f"```\n{password}\n```", 
                        inline=False
                    )
                
                await ctx.send(embed=embed)
                
            elif "FAILED" in result.stdout:
                # Zoek de error message
                error_lines = [line for line in result.stdout.split('\n') if "ERROR:" in line]
                error_msg = error_lines[0].replace("ERROR:", "").strip() if error_lines else "Onbekende fout"
                
                await status_msg.delete()
                
                if "already exists" in error_msg.lower():
                    await ctx.send(f"❌ Gebruiker **{username}** bestaat al!")
                elif "access denied" in error_msg.lower():
                    await ctx.send("❌ Toegang geweigerd! Start de bot als administrator!")
                else:
                    await ctx.send(f"❌ Fout: {error_msg}")
            else:
                # Onverwachte output, stuur debug info
                debug_embed.add_field(
                    name="📤 STDOUT",
                    value=f"```\n{result.stdout[:500]}\n```" if result.stdout else "Geen output",
                    inline=False
                )
                debug_embed.add_field(
                    name="📥 STDERR",
                    value=f"```\n{result.stderr[:500]}\n```" if result.stderr else "Geen fouten",
                    inline=False
                )
                debug_embed.add_field(
                    name="🔚 Return Code",
                    value=f"`{result.returncode}`",
                    inline=True
                )
                
                await status_msg.delete()
                await ctx.send(embed=debug_embed)
                
        except Exception as e:
            await ctx.send(f"❌ Fout: {str(e)}")

    @commands.command(name='test_powershell')
    async def test_powershell(self, ctx):
        """Test of PowerShell commands werken"""
        if not await self.check_permissions(ctx):
            return
            
        try:
            result = subprocess.run(
                ["powershell.exe", "-Command", "Get-LocalUser | Select-Object -First 1 | Format-List"],
                capture_output=True,
                text=True,
                check=False
            )
            
            embed = discord.Embed(
                title="🧪 PowerShell Test",
                color=discord.Color.blue()
            )
            
            embed.add_field(
                name="✅ Werkt PowerShell?",
                value="Ja" if result.returncode == 0 else "Nee",
                inline=True
            )
            
            embed.add_field(
                name="📤 Output",
                value=f"```\n{result.stdout[:500]}\n```" if result.stdout else "Geen output",
                inline=False
            )
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"❌ Test mislukt: {str(e)}")

async def setup(bot):
    await bot.add_cog(UserManager(bot))