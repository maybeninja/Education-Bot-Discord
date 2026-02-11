from __future__ import annotations

from datetime import timedelta

import discord
from discord import app_commands
from discord.ext import commands

from core.time_utils import now_ist
from study_assistant.setup import load_user_profile, save_user_profile


class TestAdd(commands.Cog):
    @app_commands.command(name="test_add", description="Log a completed test")
    async def test_add(self, interaction: discord.Interaction, subject: str, score: app_commands.Range[int, 0, 100], total: app_commands.Range[int, 1, 100]) -> None:
        profile = load_user_profile(interaction.user.id)
        profile.setdefault("logs", []).append(
            {"type": "test", "subject": subject, "score": score, "total": total, "ts": now_ist().isoformat()}
        )
        save_user_profile(interaction.user.id, profile)
        await interaction.response.send_message("Test logged.", ephemeral=True)


async def run_test_reminders(bot) -> None:
    now = now_ist()
    for user in bot.users:
        profile = load_user_profile(user.id)
        tests = [x for x in profile.get("logs", []) if x.get("type") == "test"]
        if not tests:
            continue
        latest = max(now.fromisoformat(x["ts"]) for x in tests)
        if now - latest >= timedelta(days=7):
            try:
                await user.send("Weekly reminder: please complete at least one test.")
            except discord.HTTPException:
                continue


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TestAdd())
