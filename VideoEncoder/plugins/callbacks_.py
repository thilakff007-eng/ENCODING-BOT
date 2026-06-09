import datetime
import json
import os

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery

from .. import app, download_dir, log, owner, sudo_users, LOGGER
from ..plugins.queue import queue_answer
from ..utils.database.access_db import db
from ..utils.settings import (
    AudioSettings,
    ExtraSettings,
    OpenSettings,
    VideoSettings
)
from .start import showw_status
from ..video_utils.audio_selector import sessions


@app.on_callback_query()
async def callback_handlers(bot: Client, cb: CallbackQuery):
    try:

        # =========================
        # FORCE JOIN FIX (IMPORTANT)
        # =========================
        if cb.data == "check":
            if await check_chat(cb.message, chat='Both'):
                await cb.message.edit_text("✅ You joined successfully. Now send /start again.")
            else:
                await cb.answer("❌ Still not joined. Join the channel first.", show_alert=True)
            return

        # =========================
        # CLOSE BUTTON
        # =========================
        if cb.data == "closeMeh":
            await cb.message.delete(True)

        # =========================
        # SETTINGS MENU
        # =========================
        elif cb.data == "VideoSettings":
            await VideoSettings(cb.message, user_id=cb.from_user.id)

        elif cb.data == "OpenSettings":
            await OpenSettings(cb.message, user_id=cb.from_user.id)

        elif cb.data == "AudioSettings":
            await AudioSettings(cb.message, user_id=cb.from_user.id)

        elif cb.data == "ExtraSettings":
            await ExtraSettings(cb.message, user_id=cb.from_user.id)

        # =========================
        # TOGGLES
        # =========================
        elif cb.data == "triggerMode":
            if await db.get_drive(cb.from_user.id):
                await db.set_drive(cb.from_user.id, drive=False)
            else:
                await db.set_drive(cb.from_user.id, drive=True)
            await ExtraSettings(cb.message, user_id=cb.from_user.id)

        elif cb.data == "triggerUploadMode":
            if await db.get_upload_as_doc(cb.from_user.id):
                await db.set_upload_as_doc(cb.from_user.id, upload_as_doc=False)
            else:
                await db.set_upload_as_doc(cb.from_user.id, upload_as_doc=True)
            await ExtraSettings(cb.message, user_id=cb.from_user.id)

        elif cb.data == "triggerResize":
            if await db.get_resize(cb.from_user.id):
                await db.set_resize(cb.from_user.id, resize=False)
            else:
                await db.set_resize(cb.from_user.id, resize=True)
            await ExtraSettings(cb.message, user_id=cb.from_user.id)

        # =========================
        # WATERMARK / METADATA
        # =========================
        elif cb.data == "triggerMetadata":
            if await db.get_metadata_w(cb.from_user.id):
                await db.set_metadata_w(cb.from_user.id, metadata=False)
            else:
                await db.set_metadata_w(cb.from_user.id, metadata=True)
            await ExtraSettings(cb.message, user_id=cb.from_user.id)

        elif cb.data == "triggerVideo":
            if await db.get_watermark(cb.from_user.id):
                await db.set_watermark(cb.from_user.id, watermark=False)
            else:
                await db.set_watermark(cb.from_user.id, watermark=True)
            await ExtraSettings(cb.message, user_id=cb.from_user.id)

        # =========================
        # SUBTITLES
        # =========================
        elif cb.data == "triggerHardsub":
            if await db.get_hardsub(cb.from_user.id):
                await db.set_hardsub(cb.from_user.id, hardsub=False)
            else:
                await db.set_hardsub(cb.from_user.id, hardsub=True)
            await ExtraSettings(cb.message, user_id=cb.from_user.id)

        elif cb.data == "triggerSubtitles":
            if await db.get_subtitles(cb.from_user.id):
                await db.set_subtitles(cb.from_user.id, subtitles=False)
            else:
                await db.set_subtitles(cb.from_user.id, subtitles=True)
            await ExtraSettings(cb.message, user_id=cb.from_user.id)

        # =========================
        # VIDEO SETTINGS
        # =========================
        elif cb.data == "triggerResolution":
            r = await db.get_resolution(cb.from_user.id)
            if r == 'OG':
                await db.set_resolution(cb.from_user.id, resolution='1080')
            elif r == '1080':
                await db.set_resolution(cb.from_user.id, resolution='720')
            elif r == '720':
                await db.set_resolution(cb.from_user.id, resolution='480')
            elif r == '480':
                await db.set_resolution(cb.from_user.id, resolution='576')
            else:
                await db.set_resolution(cb.from_user.id, resolution='OG')
            await VideoSettings(cb.message, user_id=cb.from_user.id)

        elif cb.data == "triggerHevc":
            if await db.get_hevc(cb.from_user.id):
                await db.set_hevc(cb.from_user.id, hevc=False)
            else:
                await db.set_hevc(cb.from_user.id, hevc=True)
                await cb.answer("H265 needs more time for encoding", show_alert=True)
            await VideoSettings(cb.message, user_id=cb.from_user.id)

        # =========================
        # STATS
        # =========================
        elif 'stats' in cb.data:
            stats = await showw_status(bot)
            stats = stats.replace('<b>', '').replace('</b>', '')
            await cb.answer(stats, show_alert=True)

        # =========================
        # QUEUE
        # =========================
        elif "queue+" in cb.data:
            await queue_answer(app, cb)

    except Exception as e:
        LOGGER.error(f"Error in callback_handlers: {e}")
        try:
            await cb.answer("Error occurred. Try again.", show_alert=True)
        except:
            pass
