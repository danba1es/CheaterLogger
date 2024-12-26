import discord
import json
from datetime import datetime

with open('config.json', 'r') as f:
    config = json.load(f)

class EmbedBuilder:
    @staticmethod
    def build_cheater_embed(cheater):
        embed = discord.Embed(
            title=f"{config['emojis']['reported']} Cheater Report",
            color=config['colors']['info']
        )

        embed.add_field(name="Gamertag", value=cheater['gamertag'], inline=False)
        embed.add_field(name="Reported By", value=f"<@{cheater['reporter_id']}>", inline=True)
        embed.add_field(name="Status", value="Banned" if cheater['is_banned'] else "Reported", inline=True)
        embed.add_field(name="Timestamp", value=cheater['timestamp'].strftime("%Y-%m-%d %H:%M:%S"), inline=True)

        if cheater['map_location']:
            embed.add_field(name="Map Location", value=cheater['map_location'], inline=True)
        if cheater['base_location']:
            embed.add_field(name="Base Location", value=cheater['base_location'], inline=True)
        if cheater['spi_command']:
            embed.add_field(name="SPI Command", value=f"`{cheater['spi_command']}`", inline=True)

        return embed

    @staticmethod
    def build_success_embed(message):
        return discord.Embed(
            title=f"{config['emojis']['success']} Success",
            description=message,
            color=config['colors']['success']
        )

    @staticmethod
    def build_error_embed(message):
        return discord.Embed(
            title=f"{config['emojis']['error']} Error",
            description=message,
            color=config['colors']['error']
        )

    @staticmethod
    def build_info_embed(message):
        return discord.Embed(
            title=f"{config['emojis']['warning']} Information",
            description=message,
            color=config['colors']['info']
        )