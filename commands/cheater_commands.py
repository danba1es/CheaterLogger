import discord
from discord import app_commands
from discord.ext import commands
from utils.embed_builder import EmbedBuilder
from db.database import Database
import logging

logger = logging.getLogger('bot')

class CheaterCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()

    @app_commands.command(name="cheater-log")
    async def cheater_log(self, interaction: discord.Interaction, gamertag: str):
        try:
            query = """
                INSERT INTO cheaters (gamertag, reporter_id)
                VALUES (%s, %s)
                RETURNING *
            """
            result = self.db.execute_query(query, (gamertag, interaction.user.id))
            
            await interaction.response.send_message(
                embed=EmbedBuilder.build_success_embed(f"Cheater {gamertag} has been logged!")
            )
        except Exception as e:
            logger.error(f"Error in cheater-log: {str(e)}")
            await interaction.response.send_message(
                embed=EmbedBuilder.build_error_embed("Failed to log cheater.")
            )

    @app_commands.command(name="cheaterlist")
    async def cheaterlist(self, interaction: discord.Interaction):
        try:
            query = """
                SELECT * FROM cheaters
                WHERE reporter_id = %s
                ORDER BY timestamp DESC
            """
            results = self.db.execute_query(query, (interaction.user.id,))
            
            if not results:
                await interaction.response.send_message(
                    embed=EmbedBuilder.build_info_embed("You haven't reported any cheaters yet.")
                )
                return

            embeds = []
            for cheater in results:
                embeds.append(EmbedBuilder.build_cheater_embed(cheater))

            await interaction.response.send_message(embeds=embeds[:10])
        except Exception as e:
            logger.error(f"Error in cheaterlist: {str(e)}")
            await interaction.response.send_message(
                embed=EmbedBuilder.build_error_embed("Failed to retrieve cheater list.")
            )

    @app_commands.command(name="cheaterlist-clear")
    @app_commands.checks.has_role("extra access")
    async def cheaterlist_clear(self, interaction: discord.Interaction):
        try:
            query = "DELETE FROM cheaters"
            self.db.execute_query(query)
            
            await interaction.response.send_message(
                embed=EmbedBuilder.build_success_embed("All cheater lists have been cleared.")
            )
        except Exception as e:
            logger.error(f"Error in cheaterlist-clear: {str(e)}")
            await interaction.response.send_message(
                embed=EmbedBuilder.build_error_embed("Failed to clear cheater lists.")
            )

    @app_commands.command(name="cheatercaught")
    async def cheatercaught(self, interaction: discord.Interaction, gamertag: str):
        try:
            query = """
                UPDATE cheaters
                SET is_banned = TRUE
                WHERE gamertag = %s
                RETURNING *
            """
            result = self.db.execute_query(query, (gamertag,))
            
            if result:
                await interaction.response.send_message(
                    embed=EmbedBuilder.build_success_embed(f"Cheater {gamertag} has been marked as banned!")
                )
            else:
                await interaction.response.send_message(
                    embed=EmbedBuilder.build_error_embed(f"Cheater {gamertag} not found.")
                )
        except Exception as e:
            logger.error(f"Error in cheatercaught: {str(e)}")
            await interaction.response.send_message(
                embed=EmbedBuilder.build_error_embed("Failed to mark cheater as caught.")
            )

    @app_commands.command(name="cheater-remove")
    @app_commands.checks.has_role("extra access")
    async def cheater_remove(self, interaction: discord.Interaction, gamertag: str):
        try:
            query = """
                DELETE FROM cheaters
                WHERE gamertag = %s
                RETURNING *
            """
            result = self.db.execute_query(query, (gamertag,))
            
            if result:
                await interaction.response.send_message(
                    embed=EmbedBuilder.build_success_embed(f"Cheater {gamertag} has been removed.")
                )
            else:
                await interaction.response.send_message(
                    embed=EmbedBuilder.build_error_embed(f"Cheater {gamertag} not found.")
                )
        except Exception as e:
            logger.error(f"Error in cheater-remove: {str(e)}")
            await interaction.response.send_message(
                embed=EmbedBuilder.build_error_embed("Failed to remove cheater.")
            )

    @app_commands.command(name="add")
    async def add(self, interaction: discord.Interaction, gamertag: str, map_location: str = None, 
                 base_location: str = None, spi_command: str = None):
        try:
            query = """
                UPDATE cheaters
                SET map_location = %s,
                    base_location = %s,
                    spi_command = %s
                WHERE gamertag = %s
                RETURNING *
            """
            result = self.db.execute_query(query, (map_location, base_location, spi_command, gamertag))
            
            if result:
                await interaction.response.send_message(
                    embed=EmbedBuilder.build_success_embed(f"Additional information added for {gamertag}.")
                )
            else:
                await interaction.response.send_message(
                    embed=EmbedBuilder.build_error_embed(f"Cheater {gamertag} not found.")
                )
        except Exception as e:
            logger.error(f"Error in add: {str(e)}")
            await interaction.response.send_message(
                embed=EmbedBuilder.build_error_embed("Failed to add information.")
            )

    @app_commands.command(name="cheaterfind")
    async def cheaterfind(self, interaction: discord.Interaction, gamertag: str):
        try:
            query = """
                SELECT * FROM cheaters
                WHERE gamertag ILIKE %s
            """
            results = self.db.execute_query(query, (f"%{gamertag}%",))
            
            if not results:
                await interaction.response.send_message(
                    embed=EmbedBuilder.build_error_embed(f"No cheaters found matching '{gamertag}'.")
                )
                return

            embeds = []
            for cheater in results:
                embeds.append(EmbedBuilder.build_cheater_embed(cheater))

            await interaction.response.send_message(embeds=embeds[:10])
        except Exception as e:
            logger.error(f"Error in cheaterfind: {str(e)}")
            await interaction.response.send_message(
                embed=EmbedBuilder.build_error_embed("Failed to search for cheaters.")
            )
