from __future__ import annotations

import asyncio

import discord
from discord.ext import commands

from core.config import BOT_TOKEN
from core.logger import get_logger
from core.scheduler import BotScheduler

logger = get_logger(__name__)

EXTENSIONS = [
    "school.toggle",
    "school.status",
    "school.dashboard",
    "school.attendance",
    "school.attendance_status",
    "school.class_vc",
    "school.library_core",
    "school.register",
    "school.timetable_command",
    "school.help",
    "study_assistant.setup",
    "study_assistant.chapter_list",
    "study_assistant.chapters",
    "study_assistant.notes",
    "study_assistant.practice",
    "study_assistant.revisions",
    "study_assistant.tests",
    "study_assistant.confidence",
    "study_assistant.status_chapter",
    "study_assistant.status_subject",
    "study_assistant.status_overall",
    "study_assistant.consistency",
    "study_assistant.help_prep",
    "info",
]


class EducationBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix="!", intents=intents)
        self.scheduler = BotScheduler(self)

    async def setup_hook(self) -> None:
        for ext in EXTENSIONS:
            try:
                await self.load_extension(ext)
                logger.info("Loaded extension: %s", ext)
            except Exception as exc:
                logger.exception("Failed to load extension %s: %s", ext, exc)

    async def on_ready(self) -> None:
        logger.info("Logged in as %s", self.user)
        self.scheduler.start()
        try:
            synced = await self.tree.sync()
            logger.info("Synced %s app commands", len(synced))
        except Exception as exc:
            logger.exception("Command sync failed: %s", exc)


async def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN not found in environment")
    bot = EducationBot()
    async with bot:
        await bot.start(BOT_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
