from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

from study_assistant.setup import load_user_profile, save_user_profile


class NotesStatus(commands.Cog):
    @app_commands.command(name="notes_status", description="Update notes progress percent")
    async def notes_status(self, interaction: discord.Interaction, subject: str, chapter: str, percent: app_commands.Range[int, 0, 100]) -> None:
        profile = load_user_profile(interaction.user.id)
        profile.setdefault("chapters", {}).setdefault(subject, {}).setdefault(chapter, {})["notes"] = percent
        save_user_profile(interaction.user.id, profile)
        await interaction.response.send_message("Notes status updated.", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(NotesStatus())
