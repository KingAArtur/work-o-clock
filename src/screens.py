from kivy.uix.screenmanager import Screen

from settings import SettingPreset


class MainMenuScreen(Screen):
    ...


class NewPresetScreen(Screen):
    current_preset: SettingPreset

    def on_category_checkbox_click(self, instance, value) -> None:
        ...

    def on_autodetect_checkbox_click(self, instance, value) -> None:
        ...

    def on_save(self) -> None:
        ...


class PickPresetScreen(Screen):
    ...


class ManagePresetScreen(Screen):
    ...


class StatsScreen(Screen):
    ...
