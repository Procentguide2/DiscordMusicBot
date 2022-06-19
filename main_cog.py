import discord
from discord.ext import commands
from discord import Member, guild
from discord import User
from discord.utils import get
from discord.ext.commands import has_permissions, MissingPermissions


class main_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_message = """
```
General commands:
!help - displays all the available commands
!clear amount - will delete the past messages with the amount specified
!kick - Kick member
!ban - Ban member
!unban - Unban member
!add_role - add role to some member
!del_role - remove a role from a member
!mute - mute member
!unmute - unmute member
!warn - warn members
!remove_warn - remove members warns
!edit_warn - edit member warning
!warns - show member warn statistic
Music commands:
!p <keywords> - finds the song on youtube and plays it in your current channel
!q - displays the current music queue
!skip - skips the current song being played
!disconnect - Disconnecting bot from VC
!stop - Stops the music
!pause - Pause music
!resume - Resume music
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

    @commands.command(name='create_role')
    @has_permissions(manage_roles=True)
    async def create_role_command(self, ctx, *, name):
        guild = ctx.guild
        await guild.create_role(name=name)
        await ctx.send(f'Role `{name}` has been created')

    @commands.command(name='add_role')
    @commands.has_permissions(administrator=True)
    async def add_role(self, ctx, user: discord.Member, *, role: discord.Role):
        if role in user.roles:
            await ctx.send(f"{user.mention} already has the role,{role}")
        else:
            await user.add_roles(role)  # adds role if not already has it
            await ctx.send(f"Added role {role} to {user.mention}")

    @add_role.error
    async def role_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have permission to use this command!')

    @commands.command(name='del_role')
    @commands.has_permissions(administrator=True)
    async def del_role(self, ctx, user: discord.Member, *, role: discord.Role):
        if role in user.roles:
            await user.remove_roles(role)
            await ctx.send(f"Removed role {role} from {user.mention}")
        else:
            await ctx.send(f"{user.mention} does not have the role {role}")

    @del_role.error
    async def role_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(' You do not have permission to use this command!')

    @commands.command(name='mute')
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")

        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")

            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True,
                                              read_messages=False)
        await member.add_roles(mutedRole, reason=reason)
        await ctx.send(f"Muted {member.mention} for reason {reason}")
        await member.send(f"You were muted in the server {guild.name} for {reason}")

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("You don't have the 'staff' role")

    @commands.command(name='unmute')
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx, member: discord.Member):
        mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(mutedRole)
        await ctx.send(f"Unmuted {member.mention}")
        await member.send(f"You were unmuted in the server {ctx.guild.name}")

    @unmute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("That is not a valid member")

    @commands.command(pass_context=True)
    async def invite(self, ctx):
        # Creating an invitation link
        link = await ctx.channel.create_invite(xkcd=True, max_age=0, max_uses=0)
        # max_age = 0 The invite link will never expire.
        # max_uses = 0 Infinite users can join through the link.
        # -----------------------------------------------------#

        # -------Embed Time-----#
        em = discord.Embed(title=f"Join The {ctx.guild.name} Discord Server Now!", url=link,
                           description=f"**{ctx.guild.member_count} Members** [**JOIN**]({link})\n\n**Invite link for {ctx.channel.mention} is created.**\nNumber of uses: **Infinite**\nLink Expiry Time: **Never**",
                           color=0x303037)

        # Embed Thumbnail Image
        em.set_thumbnail(url=ctx.guild.icon_url)

        # Embed Author
        em.set_author(name="INSTANT SERVER INVITE")
        # -----------------------------------------#
        await ctx.send(f"> {link}", embed=em)

    # server_info command
    @commands.command(name='info')
    @commands.has_permissions(administrator=True)
    async def server_info(self, ctx):

        # Displays server information

        embed = discord.Embed(title=f"{ctx.guild.name} Info", description="Information of this Server",
                              color=0x176cd5)
        embed.add_field(name='🆔Server ID',
                        value=f"{ctx.guild.id}", inline=True)
        embed.add_field(name='📆Created On',
                        value=ctx.guild.created_at.strftime("%b %d %Y"), inline=True)
        embed.add_field(name='👥Members',
                        value=f'{ctx.guild.member_count} Members', inline=True)
        embed.add_field(name='💬Channels',
                        value=f'{len(ctx.guild.text_channels)} Text | {len(ctx.guild.voice_channels)} Voice',
                        inline=True)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(text="⭐ • Duo")
        embed.set_author(name=f'{ctx.author.name}',
                         icon_url=ctx.message.author.avatar_url)
        await ctx.send(

            embed=embed
        )

    @commands.command(name='avatar')
    async def avatar(self, ctx, user: discord.Member = None):

        # Displays users avatar

        if not user:
            embed = discord.Embed(title="View full image.", url=ctx.message.author.avatar_url, color=0x176cd5)
            embed.set_image(url=ctx.message.author.avatar_url)
            embed.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
            await ctx.send(

                embed=embed
            )
        else:
            embed = discord.Embed(title="View full image.", url=user.avatar_url, color=0x176cd5)
            embed.set_image(url=user.avatar_url)
            embed.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
            await ctx.send(

                embed=embed

            )

