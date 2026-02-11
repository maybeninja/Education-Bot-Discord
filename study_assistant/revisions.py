from __future__ import annotations

from datetime import timedelta

import discord
from discord import app_commands
from discord.ext import commands

from core.time_utils import now_ist
from study_assistant.setup import load_user_profile, save_user_profile


class RevisionDone(commands.Cog):
    @app_commands.command(name="revision_done", description="Mark revision completion for chapter")
    async def revision_done(self, interaction: discord.Interaction, subject: str, chapter: str) -> None:
        profile = load_user_profile(interaction.user.id)
        entry = profile.setdefault("chapters", {}).setdefault(subject, {}).setdefault(chapter, {})
        entry["revisions"] = entry.get("revisions", 0) + 1
        entry["last_revision"] = now_ist().isoformat()
        save_user_profile(interaction.user.id, profile)
        await interaction.response.send_message("Revision logged.", ephemeral=True)


async def run_revision_reminders(bot) -> None:
    now = now_ist()
    for user in bot.users:
        profile = load_user_profile(user.id)
        cycle = int(profile.get("revision_cycle", 7))
        for subject, chapter_map in profile.get("chapters", {}).items():
            for chapter, payload in chapter_map.items():
                last = payload.get("last_revision")
                if not last:
                    continue
                due = now.fromisoformat(last) + timedelta(days=cycle)
                if now >= due:
                    try:
                        await user.send(f"Revision reminder: {subject} - {chapter} is due.")
                    except discord.HTTPException:
                        continue


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(RevisionDone())
