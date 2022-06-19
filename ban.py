import random
import ast
from datetime import datetime
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

# These color constants are taken from discord.js library
with open("embed_colors.txt") as f:
    data = f.read()
    colors = ast.literal_eval(data)
    color_list = [c for c in colors.values()]


class Ban(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Define a new command

    @commands.command(

        name='ban',
    )
    @commands.has_permissions(administrator=True)
    @has_permissions(manage_messages=True)
    async def ban_command(self, ctx, user: discord.Member, *, reason: str):
        if user.id == self.bot.user.id:
            # User tried to ban this exact bot.

            await ctx.send(
                "Unable to give ban to bot")

            return

        if user.bot == 1:
            # User tried to ban a bot.

            await ctx.send("It's useless to ban a bot.")

            return

        if user == ctx.author:
            # User tried to ban themselves.

            await ctx.send("Can't give a ban to yourself")

            return

        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        embed = discord.Embed(

            title=f"{user.name}'s new ban",
            color=random.choice(color_list)

        )
        embed.set_author(

            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url,
            url=f"https://discord.com/users/{ctx.message.author.id}/"

        )
        embed.add_field(

            name="Ban",
            value=f"Blocker: {ctx.author.name} (<@{ctx.author.id}>)\nReason: {reason}\nChannel: <#{str(ctx.channel.id)}>\nDate and Time: {dt_string}",
            inline=True

        )
        await user.ban(reason=reason)
        await ctx.send(

            content="Successfully added new ban.",
            embed=embed

        )

        # Creates and sends embed, showing that the user has been warned successfully.

        return

        # using "return" so that it doesn't continue along the script

    @ban_command.error
    async def ban_handler(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            # Author is missing permissions

            await ctx.send(
                '{0.author.name}, you do not have the correct permissions to do so. *(commands.MissingPermissions error, action cancelled)*'.format(
                    ctx))

            return

        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'user':
                # Author did not specify the user to ban

                await ctx.send(
                    "{0.author.name}, you forgot to specify a user to ban. *(commands.MissingRequiredArgument error, action cancelled)*".format(
                        ctx))
                return

        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'reason':
                # Author did not specify the reason

                await ctx.send(
                    "{0.author.name}, you forgot to specify a reason. *(commands.MissingRequiredArgument error, action cancelled)*".format(
                        ctx))

                return

        print(error)
        await ctx.send(error)

    @commands.command(name='unban')
    @commands.has_permissions(administrator=True)
    async def unban_command(self, ctx, *, user=None):

        def check(ms):

            # Look for the message sent in the same channel where the command was used

            # As well as by the user who used the command.

            return ms.channel == ctx.message.channel and ms.author == ctx.message.author

        try:
            user = await commands.converter.UserConverter().convert(ctx, user)
        except:
            await ctx.send("Error: user could not be found!")

            return

        await ctx.send(content='Are you sure you want to remove this ban? (Reply with y or n)'
                       )
        msg = await self.bot.wait_for('message', check=check)
        reply = msg.content.lower()  # Set the reply into a string
        if reply in ('y', 'yes', 'confirm'):
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

            await ctx.send(f"[{ctx.author.name}], user [{user.name} ({user.id})] Successfully unbanned")

        elif reply in ('n', 'no', 'cancel'):
            await ctx.send("Alright, action cancelled.")

            return

        else:
            await ctx.send("I have no idea what you want me to do. Action cancelled.")


def setup(bot):
    bot.add_cog(Ban(bot))
