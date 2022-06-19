from discord.ext import commands
import os
from dotenv import load_dotenv
from main_cog import main_cog
from music_cog import music_cog
from warn import Warn
from ban import Ban


def get_prefix(client, message):
    prefixes = ['!']  # sets the prefixes, you can keep it as an array of only 1 item if you need only one prefix

    if not message.guild:
        prefixes = ['']  # Only allow '+' as a prefix when in DMs, this is optional

    return commands.when_mentioned_or(*prefixes)(client, message)


print_messages = True

# Decides whether or not the bot shall print every message to the command prompt.

# False means that it will not print any of the user messages to the terminal

# True means that it will (at the expense of your user members' privacy, from a certain point of view).


load_dotenv()
DISCORD_TOKEN = os.getenv("discord_token")
bot = commands.Bot(

    # Create a new bot
    command_prefix=get_prefix,  # Set the prefix
    case_insensitive=True  # Make the commands case insensitive

)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


@bot.listen()
async def on_message(message):
    global print_messages
    if print_messages:
        if message.content == "":
            print(
                f'{bcolors.OKBLUE}{message.author}{bcolors.ENDC} {bcolors.OKGREEN}(#{message.channel}, {message.channel.id} in {message.guild}){bcolors.ENDC}: (no comments included)')
            if not message.attachments == "[]":
                print(message.attachments)
        else:
            print(
                f'{bcolors.OKBLUE}{message.author}{bcolors.ENDC} {bcolors.OKGREEN}(#{message.channel}, {message.channel.id} in {message.guild}){bcolors.ENDC}:\n{message.content}')
            if message.attachments:
                print(message.attachments)


# remove the default help command so that we can write out own

bot.remove_command('help')

# register the class with the bot

bot.add_cog(main_cog(bot))
bot.add_cog(music_cog(bot))
bot.add_cog(Warn(bot))
bot.add_cog(Ban(bot))

# start the bot with our token

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN, bot=True, reconnect=True)
