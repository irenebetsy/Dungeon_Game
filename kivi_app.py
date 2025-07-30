from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from functools import partial

from game.engine import GameEngine
from game.display import render_map
from game.save_load import save_level, load_level

Window.clearcolor = (0.1, 0.1, 0.1, 1)  # Dark background

class DungeonApp(App):
    def build(self):
        self.engine = GameEngine()  # Create engine instance

        self.root_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.status_label = Label(
            text=self.get_status_text(),
            size_hint=(1, 0.1),
            color=(1, 1, 1, 1),
            font_size='18sp'
        )
        self.message_label = Label(
            text='',
            size_hint=(1, 0.1),
            color=(0.8, 0.9, 1, 1),
            font_size='16sp'
        )

        self.root_layout.add_widget(self.status_label)
        self.root_layout.add_widget(self.message_label)

        self.map_label = Label(
            text=render_map(self.engine),
            font_size='20sp',
            font_name='DejaVuSansMono',
            color=(1, 1, 1, 1)
        )
        self.root_layout.add_widget(self.map_label)

        # Movement arrows
        arrow_layout = GridLayout(cols=3, rows=2, size_hint=(1, 0.3))
        arrow_layout.add_widget(Label())  # Empty
        arrow_layout.add_widget(Button(text='⬆️', on_press=partial(self.move, 'up')))
        arrow_layout.add_widget(Label())
        arrow_layout.add_widget(Button(text='⬅️', on_press=partial(self.move, 'left')))
        arrow_layout.add_widget(Button(text='⬇️', on_press=partial(self.move, 'down')))
        arrow_layout.add_widget(Button(text='➡️', on_press=partial(self.move, 'right')))
        self.root_layout.add_widget(arrow_layout)

        # Action buttons
        action_layout = GridLayout(cols=4, size_hint=(1, 0.15))
        action_layout.add_widget(Button(text="🔍 Reveal", on_press=self.reveal))
        action_layout.add_widget(Button(text="💾 Save", on_press=self.save))
        action_layout.add_widget(Button(text="📂 Load", on_press=self.load))
        action_layout.add_widget(Button(text="❌ Exit", on_press=self.stop_app))
        self.root_layout.add_widget(action_layout)

        # Allow keyboard input
        Window.bind(on_key_down=self.on_key_down)

        return self.root_layout

    def get_status_text(self):
        return f"❤️ Lives: {self.engine.lives}   💰 Coins: {self.engine.coins}"

    def update_ui(self, message=""):
        self.status_label.text = self.get_status_text()
        self.map_label.text = render_map(self.engine)
        self.message_label.text = message

    def move(self, direction, instance):
        message = self.engine.move_player(direction)
        self.update_ui(message)

    def reveal(self, instance):
        self.engine.reveal_all()
        self.update_ui("🕯️ Revealed hidden tiles!")

    def save(self, instance):
        save_level(self.engine.level)
        self.update_ui("💾 Game saved!")

    def load(self, instance):
        level = load_level()
        self.engine = GameEngine()
        self.engine.level = level
        if hasattr(self.engine, 'load_level'):
            self.engine.load_level(level)
        self.update_ui(f"📂 Loaded Level {level}")

    def stop_app(self, instance):
        App.get_running_app().stop()

    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        key_map = {
            273: 'up',
            274: 'down',
            275: 'right',
            276: 'left',
            ord('w'): 'up',
            ord('s'): 'down',
            ord('a'): 'left',
            ord('d'): 'right',
        }
        if key in key_map:
            direction = key_map[key]
            message = self.engine.move_player(direction)
            self.update_ui(message)

if __name__ == '__main__':
    DungeonApp().run()
