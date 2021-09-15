from socket import socket
from discord import Activity, ActivityType
from discord.ext import tasks
from discord.ext.commands import Cog, Bot as _bot
from modules.utils import get_logger

from mcstatus import MinecraftServer

from modules.config import Config

class Bot(Cog):
    """Main bot management commands/events
    """

    def __init__(self, bot):
        self.bot: _bot = bot
        self.fetch_server_task.start()

    @Cog.listener()
    async def on_ready(self):
        get_logger().info(f"Booted and running on user: {self.bot.user}")

    @tasks.loop(seconds = int(Config.CYCLE))
    async def fetch_server_task(self):
        try:
            server = MinecraftServer.lookup(Config.SERVER_ADDRESS)
            status = server.status()
        except socket.error:
            status = None

        await self.bot.wait_until_ready()

        if status != None:
            current_players = str(status.players.online)
            max_players = str(status.players.max)
            
            await self.bot.change_presence(
                activity=Activity(
                    type=ActivityType.watching, name=Config.STATUS_TEXT.replace('%current%', current_players).replace('%max%', max_players)
                    )
                )
        print('2')
def setup(bot: _bot):
    bot.add_cog(Bot(bot))
