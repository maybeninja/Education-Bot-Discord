from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

from school.attendance_state import get_attendance_stats
from school.state import load_school_state


class SchoolDashboard(commands.Cog):
    @app_commands.command(name="dashboard", description="Combined dashboard for school metrics")
    async def dashboard(self, interaction: discord.Interaction) -> None:
        if interaction.guild is None:
            await interaction.response.send_message("Guild-only command.", ephemeral=True)
            return
        state = load_school_state(interaction.guild.id)
        attendance = get_attendance_stats(interaction.guild.id)
        embed = discord.Embed(title="School Dashboard")
        embed.add_field(name="School Open", value=str(state.get("is_open")), inline=True)
        embed.add_field(name="Current Block", value=str(state.get("block_index")), inline=True)
        embed.add_field(name="Library Open", value=str(state.get("library_open")), inline=True)
        embed.add_field(name="Attendance Marked", value=str(attendance.get("present", 0)), inline=True)
        embed.add_field(name="Attendance Window", value=attendance.get("status", "closed"), inline=True)
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SchoolDashboard())
