"""Translation App -- Kivy application entry point.

Loads the main screen and provides language list to the KV language.
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp

from translations.languages import LANGUAGES
from ui.main_screen import MainScreen


class TranslationApp(App):
    """Main application class."""

    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)
        # Expose language display names to KV language via app.language_names
        self.language_names = list(LANGUAGES.values())

    def build(self) -> MainScreen:
        self.title = "Translator"
        self.icon = "icon.png" if self._icon_exists() else ""
        # Set minimum window size for usability
        self.minimum_width = dp(320)
        self.minimum_height = dp(480)
        return MainScreen()

    @staticmethod
    def _icon_exists() -> bool:
        import os
        return os.path.isfile("icon.png")


if __name__ == "__main__":
    TranslationApp().run()
