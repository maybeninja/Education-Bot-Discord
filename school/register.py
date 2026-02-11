from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

from study_assistant.setup import load_user_profile, save_user_profile


class RegisterSubjects(commands.Cog):
    @app_commands.command(name="register", description="Register your subjects list")
    @app_commands.describe(subjects="Comma-separated subjects")
    async def register(self, interaction: discord.Interaction, subjects: str) -> None:
        profile = load_user_profile(interaction.user.id)
        profile["subjects"] = [s.strip() for s in subjects.split(",") if s.strip()]
        save_user_profile(interaction.user.id, profile)
        await interaction.response.send_message("Subjects registered.", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(RegisterSubjects())
