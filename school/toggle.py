from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

from school.state import load_school_state, save_school_state


class SchoolToggle(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="school", description="Open or close the school system")
    @app_commands.describe(mode="open or close")
    async def school_toggle(self, interaction: discord.Interaction, mode: str) -> None:
        if interaction.guild is None:
            await interaction.response.send_message("This command is guild-only.", ephemeral=True)
            return
        mode_clean = mode.strip().lower()
        if mode_clean not in {"open", "close"}:
            await interaction.response.send_message("Use mode as `open` or `close`.", ephemeral=True)
            return
        state = load_school_state(interaction.guild.id)
        state["is_open"] = mode_clean == "open"
        if mode_clean == "close":
            state["block_index"] = -1
        save_school_state(interaction.guild.id, state)
        await interaction.response.send_message(f"School is now **{mode_clean}**.")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SchoolToggle(bot))
