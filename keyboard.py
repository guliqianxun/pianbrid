from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from kivy.core.window import Window

class Keyboard(GridLayout):
    def __init__(self, **kwargs):
        super(Keyboard, self).__init__(**kwargs)
        self.cols = 1
        self.key_map = {
            'a': 'C4',
            's': 'D4',
            'd': 'E4',
            'f': 'F4',
            'j': 'G4',
            'k': 'A4',
            'l': 'B4',
            ';': 'C5'
        }
        self.sounds = {}
        self.init_keys()
        self.load_sounds()
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def init_keys(self):
        for key in self.key_map.keys():
            button = Button(text=key)
            button.bind(on_press=lambda btn, k=key: self.play_note(self.key_map[k]))
            self.add_widget(button)

    def load_sounds(self):
        for key, note in self.key_map.items():
            sound_file = f'assets/sounds/piano_notes/{note}.wav'  
            sound = SoundLoader.load(sound_file)
            if sound:
                self.sounds[note] = sound
            else:
                print(f"Failed to load sound for {note}")

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        key = keycode[1]
        if key in self.key_map:
            self.play_note(self.key_map[key])
            return True
        return False

    def _keyboard_closed(self):
        print("Keyboard closed")
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def play_note(self, note):
        sound = self.sounds.get(note)
        if sound:
            sound.play()

# 示例使用
if __name__ == '__main__':
    class KeyboardApp(App):
        def build(self):
            return Keyboard()
    KeyboardApp().run()