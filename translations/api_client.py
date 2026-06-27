"""MyMemory Translation API client.

Handles HTTP communication with the MyMemory translation service.
All methods are synchronous -- callers must run them in a background thread.
"""

from __future__ import annotations

import logging
import urllib.parse

import requests

logger = logging.getLogger(__name__)

BASE_URL = "https://api.mymemory.translated.net/get"
REQUEST_TIMEOUT = 30


class TranslationError(Exception):
    """Raised when the API returns an error response."""

    def __init__(self, message: str, code: int | None = None) -> None:
        super().__init__(message)
        self.code = code


class APIClient:
    """Thread-safe client for the MyMemory translation API."""

    @staticmethod
    def translate(text: str, source: str, target: str) -> str:
        """Translate *text* from *source* language to *target* language.

        Parameters
        ----------
        text:
            The text to translate.
        source:
            Source language code (e.g. ``"en"``, ``"zh-CN"``).
        target:
            Target language code (e.g. ``"ja"``).

        Returns
        -------
        str
            The translated text.

        Raises
        ------
        TranslationError
            On API errors (rate limit, bad response, etc.).
        requests.exceptions.ConnectionError
            On network connectivity failures.
        requests.exceptions.Timeout
            On request timeout.
        """
        params = {
            "q": text,
            "langpair": f"{source}|{target}",
        }

        resp = requests.get(BASE_URL, params=params, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()

        data = resp.json()

        status = data.get("responseStatus", -1)
        if status == 401:
            raise TranslationError(
                "Daily translation limit reached (1000 words/day free tier). "
                "Please try again tomorrow.",
                code=401,
            )
        if status != 200:
            details = data.get("responseDetails", "Unknown error")
            raise TranslationError(
                f"Translation failed: {details}",
                code=status,
            )

        translated = data.get("data", {}).get("translatedText", "")
        # MyMemory sometimes uses "responseData" instead of "data"
        if not translated:
            translated = data.get("responseData", {}).get("translatedText", "")
        if not translated:
            raise TranslationError("Translation returned empty result.")

        return translated
