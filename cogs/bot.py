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

    @Cog.listener()
    async def on_ready(self):
        get_logger().info(f"Booted and running on user: {self.bot.user}")

        self.fetch_server_task.start()

    @tasks.loop(seconds = int(Config.CYCLE))
    async def fetch_server_task(self):
        server = MinecraftServer.lookup(Config)
        status = server.status()

        if status.players.max > 0:
            players = status.players.online
        else:
            players = status.players.online + "/" + status.players.max
        
        await self.bot.change_presence(
            activity=Activity(
                type=ActivityType.watching, name=players
                )
            )

def setup(bot: _bot):
    bot.add_cog(Bot(bot))
