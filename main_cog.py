import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions


class main_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_message = """
```
General commands:
/help - displays all the available commands
/clear amount - will delete the past messages with the amount specified
Music commands:
/p <keywords> - finds the song on youtube and plays it in your current channel
/q - displays the current music queue
/skip - skips the current song being played
/disconnect - Disconnecting bot from VC
/stop - Stops the music
/kick - Kick 
/ban - Ban
/unban - Unban
/pause - 
/resume - 
```
"""
        self.text_channel_list = []

    # some debug info so that we know the bot has started
    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                self.text_channel_list.append(channel)

        print("activated")

    @commands.command(name="help", help="Displays all the available commands")
    async def help(self, ctx):
        await ctx.send(self.help_message)

    async def send_to_all(self, msg):
        for text_channel in self.text_channel_list:
            await text_channel.send(msg)

    @commands.command(name="clear", help="Clears a specified amount of messages")
    async def clear(self, ctx, arg):
        # extract the amount to clear
        amount = 5
        try:
            amount = int(arg)
        except Exception:
            pass

        await ctx.channel.purge(limit=amount)

    @commands.command(name='kick')
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, why=None):
        await member.kick(reason=why)
        await ctx.send(f'User {member} has been kicked')

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(commands.MissingPermissions):
            await ctx.send("You don't have permission")

    @commands.command
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please pass in all requirements')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You dont have all the requirements")

    @commands.command(name='ban')
    @commands.has_permissions(administrator=True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, why=None):
        await member.ban(reason=why)

    @commands.command(name='unban')
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, user=None):

        try:
            user = await commands.converter.UserConverter().convert(ctx, user)
        except:
            await ctx.send("Error: user could not be found!")
            return

        try:
            bans = tuple(ban_entry.user for ban_entry in await ctx.guild.bans())
            if user in bans:
                await ctx.guild.unban(user, reason="Responsible moderator: " + str(ctx.author))
            else:
                await ctx.send("User not banned!")
                return

        except discord.Forbidden:
            await ctx.send("I do not have permission to unban!")
            return

        except:
            await ctx.send("Unbanning failed!")
            return

        await ctx.send(f"Successfully unbanned {user.mention}!")