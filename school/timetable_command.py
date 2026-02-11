from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

from school.timetable_engine import generate_weekly_timetable


class TimetableCommand(commands.Cog):
    @app_commands.command(name="timetable", description="View the weekly timetable")
    async def timetable(self, interaction: discord.Interaction) -> None:
        if interaction.guild is None:
            await interaction.response.send_message("Guild-only command.", ephemeral=True)
            return
        table = generate_weekly_timetable(interaction.guild.id)
        embed = discord.Embed(title="Weekly Timetable")
        for day, slots in table.items():
            summary = "\n".join(f"{x['slot']}. {x['name']} ({x['time']})" for x in slots[:6])
            embed.add_field(name=day, value=summary or "-", inline=False)
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TimetableCommand())
