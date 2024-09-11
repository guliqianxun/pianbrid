from kivy.app import App
from GameScreen import GameScreen
from StartScreen import StartScreen
from kivy.uix.screenmanager import ScreenManager, Screen

# class MainWidget(Screen):
#     def __init__(self, **kwargs):
#         super(MainWidget, self).__init__(**kwargs)
#         self.orientation = 'vertical'
#         self.add_widget(Keyboard())



class PianoApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(GameScreen(name='main'))
        return sm