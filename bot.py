import discord
from discord.ext import commands, tasks
import logging
import os
from db.database import Database
from commands.cheater_commands import CheaterCommands
from utils.config import load_config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('bot')

class CheaterBot(commands.Bot):
    def __init__(self):
        # Enable all necessary intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True  # Required for role management
        intents.guilds = True   # Required for guild operations
        super().__init__(command_prefix="!", intents=intents)

        self.config = load_config()
        self.db = Database()

    async def setup_hook(self):
        await self.add_cog(CheaterCommands(self))
        await self.tree.sync()

    async def create_extra_access_role(self, guild):
        existing_role = discord.utils.get(guild.roles, name="extra access")
        if not existing_role:
            try:
                await guild.create_role(
                    name="extra access",
                    color=discord.Color.blue(),
                    reason="Created for cheater bot management"
                )
                logger.info(f"Created 'extra access' role in guild {guild.name}")
            except Exception as e:
                logger.error(f"Failed to create role in guild {guild.name}: {str(e)}")

    async def on_ready(self):
        logger.info(f'Logged in as {self.user.name}')
        logger.info(f'Bot ID: {self.user.id}')
        logger.info('------')

        # Create roles in all guilds
        for guild in self.guilds:
            await self.create_extra_access_role(guild)

        # Initialize database
        self.db.initialize_tables()

    async def on_guild_join(self, guild):
        logger.info(f'Joined new guild: {guild.name}')
        await self.create_extra_access_role(guild)

def main():
    bot = CheaterBot()
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        raise ValueError("DISCORD_BOT_TOKEN environment variable is not set")
    bot.run(token)

if __name__ == "__main__":
    main()