from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

from school.state import load_school_state


class SchoolStatus(commands.Cog):
    @app_commands.command(name="school_status", description="View school status")
    async def school_status(self, interaction: discord.Interaction) -> None:
        if interaction.guild is None:
            await interaction.response.send_message("Guild-only command.", ephemeral=True)
            return
        state = load_school_state(interaction.guild.id)
        embed = discord.Embed(title="School Status")
        embed.add_field(name="Open", value=str(state.get("is_open")))
        embed.add_field(name="Block Index", value=str(state.get("block_index")))
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SchoolStatus())
