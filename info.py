from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands


class InfoCog(commands.Cog):
    @app_commands.command(name="info", description="Comprehensive guide for Education Bot")
    async def info(self, interaction: discord.Interaction) -> None:
        pages = [
            ("School System", "Use /school open|close, /dashboard, /attendance_status, /timetable."),
            ("Prep System", "Use /setup and chapter/test/revision tracking commands."),
            ("Commands", "School: /school /school_status /dashboard /register. Prep: /setup /overall_status /consistency."),
            ("Examples", "Example: /setup subjects:'Math,Physics' practice_types:'MCQ' test_types:'Mock'."),
        ]
        embed = discord.Embed(title="Education Bot Info", description="Use this as your in-app guide.")
        for title, text in pages:
            embed.add_field(name=title, value=text, inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(InfoCog())
