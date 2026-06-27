"""Main screen widget for the translation app.

Provides the UI logic for language selection, text input, translation
trigger, language swapping, and output display with copy support.
"""

from __future__ import annotations

import logging
from kivy.core.clipboard import Clipboard
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from translations.languages import (
    DISPLAY_TO_CODE,
    LANGUAGES,
    MAX_CHARS,
    RTL_LANGUAGES,
)
from translations.translator import translate_async

logger = logging.getLogger(__name__)


class MainScreen(BoxLayout):
    """Primary application screen with translation controls."""

    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self.source_code = "en"
        self.target_code = "zh-CN"
        self.is_translating = False
        self._last_input_text = ""
        self._last_output_text = ""

    # -- Language selection ------------------------------------------------

    def on_source_language_changed(self, spinner: Spinner, text: str) -> None:
        """Called when the source language spinner selection changes."""
        self.source_code = DISPLAY_TO_CODE.get(text, "en")

    def on_target_language_changed(self, spinner: Spinner, text: str) -> None:
        """Called when the target language spinner selection changes."""
        self.target_code = DISPLAY_TO_CODE.get(text, "zh-CN")

    # -- Translation ------------------------------------------------------

    def on_translate(self) -> None:
        """Trigger translation of the input text."""
        input_widget: TextInput = self.ids.input_text  # type: ignore[attr-defined]
        output_label: Label = self.ids.output_label  # type: ignore[attr-defined]
        translate_btn: Label = self.ids.translate_btn  # type: ignore[attr-defined]

        text = input_widget.text.strip()

        # Guard: empty input
        if not text:
            output_label.text = "请输入要翻译的文本 / Please enter text to translate"
            output_label.color = (1.0, 0.6, 0.0, 1.0)  # orange
            return

        # Guard: same language
        if self.source_code == self.target_code:
            output_label.text = "源语言和目标语言相同 / Source and target languages are the same"
            output_label.color = (1.0, 0.6, 0.0, 1.0)
            return

        # Guard: already translating
        if self.is_translating:
            return

        # Guard: text too long
        if len(text) > MAX_CHARS:
            output_label.text = (
                f"文本过长（最多 {MAX_CHARS} 个字符）/ Text too long (max {MAX_CHARS} chars)"
            )
            output_label.color = (1.0, 0.0, 0.0, 1.0)
            return

        # Save input for swap support
        self._last_input_text = text
        self._last_output_text = ""

        # Update UI to loading state
        self.is_translating = True
        translate_btn.text = "翻译中..."
        translate_btn.disabled = True
        output_label.color = (0.3, 0.3, 0.3, 1.0)
        output_label.text = "翻译中... / Translating..."

        # Perform async translation
        translate_async(
            text=text,
            source=self.source_code,
            target=self.target_code,
            on_result=self._on_translation_success,
            on_error=self._on_translation_error,
        )

    def _on_translation_success(self, translated: str) -> None:
        """Handle successful translation result on the main thread."""
        self.is_translating = False
        self._last_output_text = translated

        output_label: Label = self.ids.output_label  # type: ignore[attr-defined]
        translate_btn: Label = self.ids.translate_btn  # type: ignore[attr-defined]

        # Detect RTL and adjust alignment
        if self._is_rtl(translated):
            output_label.halign = "right"
        else:
            output_label.halign = "left"

        output_label.text = translated
        output_label.color = (0.1, 0.1, 0.1, 1.0)  # dark gray
        translate_btn.text = "翻译 / Translate"
        translate_btn.disabled = False

    def _on_translation_error(self, error_msg: str) -> None:
        """Handle translation error on the main thread."""
        self.is_translating = False

        output_label: Label = self.ids.output_label  # type: ignore[attr-defined]
        translate_btn: Label = self.ids.translate_btn  # type: ignore[attr-defined]

        output_label.text = error_msg
        output_label.color = (1.0, 0.0, 0.0, 1.0)  # red
        output_label.halign = "left"
        translate_btn.text = "翻译 / Translate"
        translate_btn.disabled = False

    # -- Utilities --------------------------------------------------------

    def on_swap_languages(self) -> None:
        """Swap source and target languages, and swap input/output text."""
        # Swap language codes
        self.source_code, self.target_code = self.target_code, self.source_code

        # Swap text: output becomes new input, clear output
        output_text = self._last_output_text
        input_text = self._last_input_text

        input_widget: TextInput = self.ids.input_text  # type: ignore[attr-defined]
        output_label: Label = self.ids.output_label  # type: ignore[attr-defined]

        # Update spinners to reflect swapped languages
        source_spinner: Spinner = self.ids.source_spinner  # type: ignore[attr-defined]
        target_spinner: Spinner = self.ids.target_spinner  # type: ignore[attr-defined]

        source_display = LANGUAGES.get(self.source_code, self.source_code)
        target_display = LANGUAGES.get(self.target_code, self.target_code)

        source_spinner.text = source_display
        target_spinner.text = target_display

        # Swap text content
        if output_text:
            input_widget.text = output_text
            self._last_input_text = output_text
            output_label.text = ""
            self._last_output_text = ""
        else:
            # Just swap placeholder
            input_widget.text = input_text
            output_label.text = ""

        # Reset alignment
        output_label.halign = "left"
        output_label.color = (0.3, 0.3, 0.3, 1.0)

    def on_copy_output(self) -> None:
        """Copy the translated output to clipboard."""
        text_to_copy = self._last_output_text
        if text_to_copy:
            Clipboard.copy(text_to_copy)

    @staticmethod
    def _is_rtl(text: str) -> bool:
        """Check if text contains right-to-left characters."""
        rtl_ranges = [(0x0600, 0x06FF), (0x0590, 0x05FF)]  # Arabic, Hebrew
        return any(low <= ord(ch) <= high for ch in text for low, high in rtl_ranges)
