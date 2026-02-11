from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

from study_assistant.setup import load_user_profile


class SubjectStatus(commands.Cog):
    @app_commands.command(name="subject_status", description="Aggregate status by subject")
    async def subject_status(self, interaction: discord.Interaction, subject: str) -> None:
        profile = load_user_profile(interaction.user.id)
        chapters = profile.get("chapters", {}).get(subject, {})
        if not chapters:
            await interaction.response.send_message("Subject not found.", ephemeral=True)
            return
        total_notes = sum(x.get("notes", 0) for x in chapters.values())
        total_practice = sum(x.get("practice", 0) for x in chapters.values())
        embed = discord.Embed(title=f"Subject Status: {subject}")
        embed.add_field(name="Chapters", value=str(len(chapters)))
        embed.add_field(name="Notes Progress Sum", value=str(total_notes))
        embed.add_field(name="Practice Total", value=str(total_practice))
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SubjectStatus())
