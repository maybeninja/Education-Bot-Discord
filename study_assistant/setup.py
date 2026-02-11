from __future__ import annotations

from pathlib import Path

import discord
from discord import app_commands
from discord.ext import commands

from core.config import USERS_DIR
from core.json_store import load_json, save_json


def _user_file(user_id: int) -> Path:
    return USERS_DIR / str(user_id) / "profile.json"


def load_user_profile(user_id: int) -> dict:
    default = {
        "subjects": [],
        "practice_types": [],
        "test_types": [],
        "revision_cycle": 7,
        "cutoff_hour": 22,
        "chapters": {},
        "logs": [],
    }
    payload = load_json(_user_file(user_id), default)
    for k, v in default.items():
        payload.setdefault(k, v)
    return payload


def save_user_profile(user_id: int, payload: dict) -> None:
    save_json(_user_file(user_id), payload)


class SetupCog(commands.Cog):
    @app_commands.command(name="setup", description="One-time prep assistant setup")
    async def setup_command(
        self,
        interaction: discord.Interaction,
        subjects: str,
        practice_types: str,
        test_types: str,
        revision_cycle: app_commands.Range[int, 1, 30],
        cutoff_hour: app_commands.Range[int, 0, 23],
    ) -> None:
        profile = load_user_profile(interaction.user.id)
        profile["subjects"] = [x.strip() for x in subjects.split(",") if x.strip()]
        profile["practice_types"] = [x.strip() for x in practice_types.split(",") if x.strip()]
        profile["test_types"] = [x.strip() for x in test_types.split(",") if x.strip()]
        profile["revision_cycle"] = revision_cycle
        profile["cutoff_hour"] = cutoff_hour
        save_user_profile(interaction.user.id, profile)
        await interaction.response.send_message("Setup saved.", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SetupCog())
