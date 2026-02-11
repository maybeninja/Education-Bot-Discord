from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

from study_assistant.setup import load_user_profile


class ChapterList(commands.Cog):
    @app_commands.command(name="chapter_list", description="List all chapters for your subjects")
    async def chapter_list(self, interaction: discord.Interaction) -> None:
        profile = load_user_profile(interaction.user.id)
        chapters = profile.get("chapters", {})
        if not chapters:
            await interaction.response.send_message("No chapters found.", ephemeral=True)
            return
        text = "\n".join(f"**{sub}**: {', '.join(names.keys())}" for sub, names in chapters.items())
        await interaction.response.send_message(text, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ChapterList())
