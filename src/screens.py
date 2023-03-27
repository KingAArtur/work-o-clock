from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button

from settings import (
    AppCategory, SettingPreset,
    delete_preset, edit_preset, load_preset, load_presets, store_preset,
    DEFAULT_PRESETS,
)


__all__ = (
    'ManagePresetScreen',
    'MainMenuScreen',
    'NewPresetScreen',
    'PickPresetScreen',
    'StatsScreen',
)


CHECKBOX_TO_CATEGORY = {
    'cb_messenger': AppCategory.MESSENGER,
    'cb_game': AppCategory.GAME,
    'cb_video': AppCategory.VIDEO,
    'cb_music': AppCategory.MUSIC,
    'cb_study': AppCategory.STUDY,
}


class MainMenuScreen(Screen):
    ...


class NewPresetScreen(Screen):
    def on_save(self) -> None:
        preset_name = self.ids['name_input'].text
        if not preset_name:
            # show pop-up error msg
            return

        block_categories = frozenset(
            category
            for idname, category in CHECKBOX_TO_CATEGORY.items()
            if self.ids[idname].active
        )
        preset = SettingPreset(
            name=preset_name,
            block_categories=block_categories,
            autodetect=self.ids['cb_autodetect'].active,
        )
        store_preset(preset)

        self.parent.current = 'main'


class PickPresetScreen(Screen):
    def on_enter(self) -> None:
        self.btn_dropdown.text = ''
        self.dropdown.dismiss()
        self.dropdown.clear_widgets()
        presets = load_presets()
        for preset_name in presets:
            button = Button(
                text=preset_name,
                font_size=20,
                size_hint_y=None,
                height=30,
            )
            button.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(button)

    def on_select(self, preset_name: str) -> None:
        preset = load_preset(preset_name)
        self.ids['cb_enable'].active = preset.enable
        self.btn_dropdown.text = preset_name

    def on_save(self) -> None:
        preset_name = self.btn_dropdown.text
        if not preset_name:
            # show pop-up error msg
            return

        preset = load_preset(preset_name)
        preset.enable = self.ids['cb_enable'].active
        edit_preset(preset_name, preset)

        self.parent.current = 'main'


class ManagePresetScreen(Screen):
    def on_enter(self) -> None:
        self.btn_dropdown.text = ''
        self.dropdown.dismiss()
        self.dropdown.clear_widgets()
        presets = load_presets()
        for preset_name in presets:
            if preset_name not in DEFAULT_PRESETS:
                button = Button(
                    text=preset_name,
                    font_size=20,
                    size_hint_y=None,
                    height=30,
                )
                button.bind(on_release=lambda btn: self.dropdown.select(btn.text))
                self.dropdown.add_widget(button)

    def on_select(self, preset_name: str) -> None:
        preset = load_preset(preset_name)
        self.btn_dropdown.text = preset_name

        self.ids['name_input'].text = preset.name
        for idname, category in CHECKBOX_TO_CATEGORY.items():
            self.ids[idname].active = category in preset.block_categories
        self.ids['cb_autodetect'].active = preset.autodetect

    def on_save(self) -> None:
        old_preset_name = self.btn_dropdown.text
        preset_name = self.ids['name_input'].text
        if not old_preset_name or not preset_name:
            # show pop-up error msg
            return

        block_categories = frozenset(
            category
            for idname, category in CHECKBOX_TO_CATEGORY.items()
            if self.ids[idname].active
        )
        preset = SettingPreset(
            name=preset_name,
            block_categories=block_categories,
            autodetect=self.ids['cb_autodetect'].active,
        )
        edit_preset(old_preset_name, preset)

        self.parent.current = 'main'

    def on_delete(self) -> None:
        preset_name = self.btn_dropdown.text
        if not preset_name:
            # show pop-up error msg
            return

        delete_preset(preset_name)

        self.parent.current = 'main'


class StatsScreen(Screen):
    ...
