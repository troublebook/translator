"""Translation service -- orchestrates API calls on background threads.

Provides a thread-safe interface that bridges the UI layer (main thread)
and the API client (background thread).  Results and errors are delivered
via callback scheduled on the Kivy main thread via ``Clock.schedule_once``.
"""

from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Callable

from kivy.clock import Clock

from .api_client import APIClient, TranslationError

logger = logging.getLogger(__name__)

# Single-thread executor -- translations are sequential per app instance
_executor: ThreadPoolExecutor | None = None


def _get_executor() -> ThreadPoolExecutor:
    global _executor
    if _executor is None or _executor._shutdown:
        _executor = ThreadPoolExecutor(max_workers=1)
    return _executor


def translate_async(
    text: str,
    source: str,
    target: str,
    on_result: Callable[[str], None],
    on_error: Callable[[str], None] | None = None,
) -> None:
    """Start an asynchronous translation.

    Parameters
    ----------
    text:
        Text to translate.
    source:
        Source language code.
    target:
        Target language code.
    on_result:
        Callback invoked on the **main** thread with the translated text.
    on_error:
        Optional callback invoked on the **main** thread with an error message.
        If omitted, errors are logged only.
    """
    if on_error is None:
        on_error = lambda msg: logger.error("Translation error: %s", msg)

    def _worker() -> None:
        try:
            result = APIClient.translate(text, source, target)
            Clock.schedule_once(lambda _: on_result(result), 0)
        except TranslationError as exc:
            Clock.schedule_once(lambda _: on_error(str(exc)), 0)
        except Exception as exc:
            logger.exception("Unexpected translation failure")
            Clock.schedule_once(lambda _: on_error(str(exc)), 0)

    _get_executor().submit(_worker)
