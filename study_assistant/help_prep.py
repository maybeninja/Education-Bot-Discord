from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands


class PrepHelp(commands.Cog):
    @app_commands.command(name="prep_help", description="Help for prep assistant")
    async def prep_help(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(
            title="Prep Help",
            description="Use /setup then /add_chapter, /notes_status, /practice_update, /revision_done, /test_add.",
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(PrepHelp())
