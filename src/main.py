from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FallOutTransition

from screens import MainMenuScreen, ManagePresetScreen, NewPresetScreen, PickPresetScreen, StatsScreen
from settings import init_preset_storage


class WorkOClockApp(App):
    def build(self) -> ScreenManager:
        init_preset_storage()

        sm = ScreenManager(transition=FallOutTransition(duration=0.15))
        sm.add_widget(MainMenuScreen(name='main'))
        sm.add_widget(NewPresetScreen(name='new'))
        sm.add_widget(PickPresetScreen(name='pick'))
        sm.add_widget(ManagePresetScreen(name='manage'))
        sm.add_widget(StatsScreen(name='stats'))

        return sm


if __name__ == '__main__':
    app = WorkOClockApp()
    app.run()
