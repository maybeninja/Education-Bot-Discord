from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

from core.time_utils import now_ist
from study_assistant.setup import load_user_profile, save_user_profile


class PracticeUpdate(commands.Cog):
    @app_commands.command(name="practice_update", description="Log practice count for chapter")
    async def practice_update(self, interaction: discord.Interaction, subject: str, chapter: str, count: int) -> None:
        profile = load_user_profile(interaction.user.id)
        entry = profile.setdefault("chapters", {}).setdefault(subject, {}).setdefault(chapter, {})
        entry["practice"] = entry.get("practice", 0) + max(0, count)
        profile.setdefault("logs", []).append({"type": "practice", "count": count, "ts": now_ist().isoformat()})
        save_user_profile(interaction.user.id, profile)
        await interaction.response.send_message("Practice updated.", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(PracticeUpdate())
