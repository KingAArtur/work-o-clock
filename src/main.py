from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FallOutTransition
from kivy.utils import platform

from screens import MainMenuScreen, ManagePresetScreen, NewPresetScreen, PickPresetScreen, StatsScreen


class WorkOClockApp(App):
    def build(self) -> ScreenManager:
        sm = ScreenManager(transition=FallOutTransition(duration=0.15))

        sm.add_widget(MainMenuScreen(name='main'))
        sm.add_widget(NewPresetScreen(name='new'))
        sm.add_widget(PickPresetScreen(name='pick'))
        sm.add_widget(ManagePresetScreen(name='manage'))
        sm.add_widget(StatsScreen(name='stats'))

        if platform == 'android':
            from android import AndroidService
            service = AndroidService('my pong service', 'running')
            service.start('service started')
            self.service = service

        return sm


if __name__ == '__main__':
    app = WorkOClockApp()
    app.run()
