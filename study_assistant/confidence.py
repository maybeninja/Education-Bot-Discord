from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

from study_assistant.setup import load_user_profile, save_user_profile


class Confidence(commands.Cog):
    @app_commands.command(name="confidence", description="Set confidence rating (1-10)")
    async def confidence(self, interaction: discord.Interaction, subject: str, chapter: str, rating: app_commands.Range[int, 1, 10]) -> None:
        profile = load_user_profile(interaction.user.id)
        profile.setdefault("chapters", {}).setdefault(subject, {}).setdefault(chapter, {})["confidence"] = rating
        save_user_profile(interaction.user.id, profile)
        await interaction.response.send_message("Confidence updated.", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Confidence())
