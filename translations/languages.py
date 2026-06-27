"""Supported languages for the translator.

Maps display names to MyMemory API language codes.
Ordered by frequency of use.
"""

LANGUAGES: dict[str, str] = {
    "en": "English",
    "zh-CN": "Chinese (Simplified)",
    "zh-TW": "Chinese (Traditional)",
    "ja": "Japanese",
    "ko": "Korean",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "pt": "Portuguese",
    "it": "Italian",
    "ru": "Russian",
    "ar": "Arabic",
    "hi": "Hindi",
    "vi": "Vietnamese",
    "th": "Thai",
    "id": "Indonesian",
    "tr": "Turkish",
    "pl": "Polish",
    "nl": "Dutch",
    "uk": "Ukrainian",
    "sv": "Swedish",
    "he": "Hebrew",
    "ms": "Malay",
    "fil": "Filipino",
}

# Reverse lookup: display name -> code
DISPLAY_TO_CODE: dict[str, str] = {v: k for k, v in LANGUAGES.items()}

# Languages that use right-to-left text direction
RTL_LANGUAGES: set[str] = {"ar", "he"}

# MyMemory API character limit for free tier
MAX_CHARS = 500
