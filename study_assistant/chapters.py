from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

from study_assistant.setup import load_user_profile, save_user_profile


class ChapterAdd(commands.Cog):
    @app_commands.command(name="add_chapter", description="Add a chapter under a subject")
    async def add_chapter(self, interaction: discord.Interaction, subject: str, chapter: str) -> None:
        profile = load_user_profile(interaction.user.id)
        chapters = profile.setdefault("chapters", {})
        subject_map = chapters.setdefault(subject, {})
        subject_map.setdefault(chapter, {"notes": 0, "practice": 0, "revisions": 0, "tests": 0, "confidence": 5})
        save_user_profile(interaction.user.id, profile)
        await interaction.response.send_message(f"Added chapter **{chapter}** in **{subject}**", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ChapterAdd())
