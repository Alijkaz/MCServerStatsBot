import sys
from os import listdir

from discord import Intents
from discord.ext.commands import Bot

from modules.config import Config, Env

def run_discord_bot():
    """ Running discord bot

    Notes:
        - help_command is None so that we can introduce the command later
        - Having intents.all() makes it possible to do mass actions with members
        - Will load every single cog in ~/cogs/ directory and run the bot    
    """ 
    
    bot = Bot(command_prefix=Config.PREFIX,
              intents=Intents().all(), help_command=None)

    for filename in listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
            print(f"\n- Loaded {filename}")

    bot.run(Env.TOKEN)

    return bot


if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) == 0:
        sys.exit(
            "You have not entered any args.\nAvailable args: [run , test]")

    if args[0] == 'run':
        bot = run_discord_bot()


    elif args[0] == 'test':
        from tests.test_basic import *
