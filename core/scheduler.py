from __future__ import annotations

from discord.ext import tasks

from core.logger import get_logger
from school.attendance_state import process_attendance_windows
from school.class_vc import sync_class_voice_channels
from school.engine import process_period_transitions
from school.library_cleanup import run_library_cleanup
from school.status_engine import refresh_all_status_channels
from study_assistant.revisions import run_revision_reminders
from study_assistant.tests import run_test_reminders

logger = get_logger(__name__)


class BotScheduler:
    def __init__(self, bot):
        self.bot = bot

    def start(self) -> None:
        if not self.fast_loop.is_running():
            self.fast_loop.start()
        if not self.slow_loop.is_running():
            self.slow_loop.start()

    def stop(self) -> None:
        self.fast_loop.cancel()
        self.slow_loop.cancel()

    @tasks.loop(seconds=30)
    async def fast_loop(self) -> None:
        await process_period_transitions(self.bot)
        await process_attendance_windows(self.bot)
        await sync_class_voice_channels(self.bot)
        await refresh_all_status_channels(self.bot)

    @tasks.loop(hours=1)
    async def slow_loop(self) -> None:
        await run_library_cleanup(self.bot)
        await run_revision_reminders(self.bot)
        await run_test_reminders(self.bot)

    @fast_loop.before_loop
    @slow_loop.before_loop
    async def before_any_loop(self) -> None:
        await self.bot.wait_until_ready()
        logger.info("Scheduler loops started")
