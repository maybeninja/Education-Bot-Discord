from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

from school.attendance_state import load_attendance


class AttendanceStatus(commands.Cog):
    @app_commands.command(name="attendance_status", description="View attendance window stats")
    async def attendance_status(self, interaction: discord.Interaction) -> None:
        if interaction.guild is None:
            await interaction.response.send_message("Guild-only command.", ephemeral=True)
            return
        payload = load_attendance(interaction.guild.id)
        await interaction.response.send_message(
            f"Attendance is **{'open' if payload.get('is_open') else 'closed'}**. Present marked: {len(payload.get('present_users', []))}"
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AttendanceStatus())
