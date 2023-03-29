from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FallOutTransition
from kivy.utils import platform
from kivy.properties import ObjectProperty

from jnius import autoclass
from oscpy.client import OSCClient
from oscpy.server import OSCThreadServer

from screens import MainMenuScreen, ManagePresetScreen, NewPresetScreen, PickPresetScreen, StatsScreen


SERVICE_NAME = u'{packagename}.Service{servicename}'.format(
    packagename=u'org.kivy.oscservice',
    servicename=u'Pong'
)

class WorkOClockApp(App):
    message = ObjectProperty("wait what")

    def build(self) -> ScreenManager:
        sm = ScreenManager(transition=FallOutTransition(duration=0.15))

        sm.add_widget(MainMenuScreen(name='main'))
        sm.add_widget(NewPresetScreen(name='new'))
        sm.add_widget(PickPresetScreen(name='pick'))
        sm.add_widget(ManagePresetScreen(name='manage'))
        sm.add_widget(StatsScreen(name='stats'))

        self.service = None
        self.start_service()

        server = OSCThreadServer()
        server.listen(
            address=b'localhost',
            port=3002,
            default=True,
        )
        server.bind(b'/message', self.display_message)
        server.bind(b'/date', self.date)

        self.server = server
        self.client = OSCClient(b'localhost', 3000)

        return sm

    def start_service(self):
        if platform == 'android':
            service = autoclass(SERVICE_NAME)
            self.mActivity = autoclass(u'org.kivy.android.PythonActivity').mActivity
            argument = ''
            service.start(self.mActivity, argument)
            self.service = service

        elif platform in ('linux', 'linux2', 'macos', 'win'):
            from runpy import run_path
            from threading import Thread
            self.service = Thread(
                target=run_path,
                args=['src/service/main.py'],
                kwargs={'run_name': '__main__'},
                daemon=True,
            )
            self.service.start()
        else:
            raise NotImplementedError(
                "service start not implemented on this platform"
            )

    def send(self, *args):
        self.client.send_message(b'/ping', [])

    def display_message(self, message):
        self.message = message.decode('utf8')

    def date(self, message):
        self.message = message.decode('utf8')


if __name__ == '__main__':
    app = WorkOClockApp()
    app.run()
