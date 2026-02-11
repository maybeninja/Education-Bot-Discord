from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

from study_assistant.setup import load_user_profile


class OverallStatus(commands.Cog):
    @app_commands.command(name="overall_status", description="Overall prep status")
    async def overall_status(self, interaction: discord.Interaction) -> None:
        profile = load_user_profile(interaction.user.id)
        chapter_count = sum(len(x) for x in profile.get("chapters", {}).values())
        tests = len([x for x in profile.get("logs", []) if x.get("type") == "test"])
        embed = discord.Embed(title="Overall Status")
        embed.add_field(name="Subjects", value=str(len(profile.get("subjects", []))))
        embed.add_field(name="Chapters", value=str(chapter_count))
        embed.add_field(name="Tests Logged", value=str(tests))
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(OverallStatus())
