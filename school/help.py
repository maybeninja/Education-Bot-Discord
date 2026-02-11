from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands


class SchoolHelp(commands.Cog):
    @app_commands.command(name="school_help", description="Get school system help")
    async def school_help(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title="School Help", description="Use /school open|close, /dashboard, /attendance_status, /timetable")
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SchoolHelp())
