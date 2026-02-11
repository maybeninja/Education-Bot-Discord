from __future__ import annotations

from datetime import timedelta

import discord
from discord import app_commands
from discord.ext import commands

from core.time_utils import now_ist
from study_assistant.setup import load_user_profile


class Consistency(commands.Cog):
    @app_commands.command(name="consistency", description="View 7-day and 30-day activity consistency")
    async def consistency(self, interaction: discord.Interaction) -> None:
        profile = load_user_profile(interaction.user.id)
        logs = profile.get("logs", [])
        now = now_ist()
        d7 = sum(1 for x in logs if now - now.fromisoformat(x["ts"]) <= timedelta(days=7))
        d30 = sum(1 for x in logs if now - now.fromisoformat(x["ts"]) <= timedelta(days=30))
        await interaction.response.send_message(
            f"Consistency\n7-day activity: {d7}\n30-day activity: {d30}", ephemeral=True
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Consistency())
