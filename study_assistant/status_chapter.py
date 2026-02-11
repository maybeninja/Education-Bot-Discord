from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

from study_assistant.setup import load_user_profile


class ChapterStatus(commands.Cog):
    @app_commands.command(name="chapter_status", description="Detailed status of a chapter")
    async def chapter_status(self, interaction: discord.Interaction, subject: str, chapter: str) -> None:
        profile = load_user_profile(interaction.user.id)
        data = profile.get("chapters", {}).get(subject, {}).get(chapter)
        if not data:
            await interaction.response.send_message("Chapter not found.", ephemeral=True)
            return
        embed = discord.Embed(title=f"{subject} - {chapter}")
        for k in ["notes", "practice", "revisions", "tests", "confidence"]:
            embed.add_field(name=k.title(), value=str(data.get(k, 0)))
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ChapterStatus())
