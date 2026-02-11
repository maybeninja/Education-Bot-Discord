from __future__ import annotations

from discord.ext import commands

from school.attendance_state import load_attendance, mark_attendance


class AttendanceListener(commands.Cog):
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.guild is None:
            return
        if message.content.strip().lower() not in {"yes", "present", "here"}:
            return
        payload = load_attendance(message.guild.id)
        if not payload.get("is_open"):
            return
        if mark_attendance(message.guild.id, message.author.id):
            await message.add_reaction("✅")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AttendanceListener())
