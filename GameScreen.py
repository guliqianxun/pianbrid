from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
from kivy.core.window import Window

import random

# Bird class and helper functions
class Bird:
    def __init__(self, notes_b, rarity):
        self.notes_b = notes_b
        self.rarity = rarity
        self.attraction_level = 0

    def __str__(self):
        return f"Bird with notes: {self.notes_b}, rarity: {self.rarity}, attraction level: {self.attraction_level}"

def generate_birds(M):
    notes = ['A', 'S', 'D', 'F', 'J', 'K', 'L', ';']
    birds = []
    for _ in range(M):
        notes_b_length = random.randint(1, 5)
        notes_b = ''.join([random.choice(notes) for _ in range(notes_b_length)])
        rarity = notes_b_length
        birds.append(Bird(notes_b, rarity))
    return birds

class Keyboard(GridLayout):
    def __init__(self, **kwargs):
        super(Keyboard, self).__init__(**kwargs)
        self.cols = 1
        self.rows = 10  # Adding rows to separate keys and labels
        self.key_map = {'a': 'C4', 's': 'D4', 'd': 'E4', 'f': 'F4', 'j': 'G4', 'k': 'A4', 'l': 'B4', ';': 'C5'}
        self.sounds = {}
        self.init_keys()
        self.load_sounds()
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.user_notes = []  # Store user notes input
        self.birds = generate_birds(20)  # Generate birds at start
        self.all_birds_label = Label(text="All birds: " + ', '.join([bird.notes_b for bird in self.birds]))
        self.add_widget(self.all_birds_label)
        self.captured_birds_label = Label(text="Captured birds: ")
        self.add_widget(self.captured_birds_label)

    def init_keys(self):
        for key in self.key_map.keys():
            button = Button(text=key)
            button.bind(on_press=lambda btn, k=key: self.add_note_and_play(self.key_map[k]))
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
            self.add_note_and_play(self.key_map[key])
            return True
        return False

    def _keyboard_closed(self):
        print("Keyboard closed")
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def add_note_and_play(self, note):
        sound = self.sounds.get(note)
        if sound:
            sound.play()
        if len(self.user_notes) < 10:  # Limit input to 10 notes
            self.user_notes.append(note)
        if len(self.user_notes) == 10:  # Trigger game logic when 10 notes are inputted
            self.process_game_logic()

    def process_game_logic(self):
        Notes_N = ''.join(self.user_notes)  # Combine all notes into a single string
        for bird in self.birds:
            max_length = self.find_longest_substring_match_dp(Notes_N, bird.notes_b)
            max_possible_length = len(bird.notes_b)
            score = self.calculate_score(max_length)
            max_score = self.calculate_score(max_possible_length)
            bird.attraction_level = score / max_score if max_score != 0 else 0
        
        captured_birds = [bird for bird in self.birds if bird.attraction_level >= 0.8]
        self.captured_birds_label.text = "Captured birds: " + ', '.join([bird.notes_b for bird in captured_birds])
        self.user_notes = []  # Reset notes for next round

    def find_longest_substring_match_dp(self, string_n, string_b):
        len_n = len(string_n)
        len_b = len(string_b)
        dp = [[0] * (len_b + 1) for _ in range(len_n + 1)]
        max_length = 0
        for i in range(1, len_n + 1):
            for j in range(1, len_b + 1):
                if string_n[i - 1] == string_b[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                    max_length = max(max_length, dp[i][j])
                else:
                    dp[i][j] = 0
        return max_length

    def calculate_score(self, max_length):
        return sum(10**k for k in range(max_length))

if __name__ == '__main__':
    class KeyboardApp(App):
        def build(self):
            return Keyboard()
    KeyboardApp().run()
