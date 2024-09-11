from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.screenmanager import Screen


class StartScreen(Screen):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        self.add_widgets()

    def add_widgets(self):
        # 添加开始按钮
        start_button = Button(
            text="Start Game",
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.3}
        )
        start_button.bind(on_press=self.start_game)
        self.add_widget(start_button)

        # 添加游戏说明标签
        instructions = Label(
            text="Welcome to Piano Bird! Press the start button to play.\n"
                 "This game will help you learn piano notes and rhythm.",
            size_hint=(0.8, 0.2),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.add_widget(instructions)

    def start_game(self, instance):
        app = App.get_running_app()
        app.root.current = 'main' 