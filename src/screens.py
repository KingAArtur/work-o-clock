from pathlib import Path

from kivy.uix.screenmanager import Screen

from settings import AppCategory, SettingPreset


class MainMenuScreen(Screen):
    ...


class NewPresetScreen(Screen):
    __cb2category = {
        'cb_messenger': AppCategory.MESSENGER,
        'cb_game': AppCategory.GAME,
        'cb_video': AppCategory.VIDEO,
        'cb_music': AppCategory.MUSIC,
        'cb_study': AppCategory.STUDY,
    }

    def on_save(self) -> None:
        block_categories = frozenset(
            category
            for idname, category in self.__cb2category.items()
            if self.ids[idname].active
        )

        preset = SettingPreset(
            name=self.ids['name_input'].text,
            block_categories=block_categories,
            autodetect=self.ids['cb_autodetect'].active,
        )

        # preset.to_json() - store
        print(preset)

        self.parent.current = 'main'


class PickPresetScreen(Screen):
    ...


class ManagePresetScreen(Screen):
    ...


class StatsScreen(Screen):
    ...
