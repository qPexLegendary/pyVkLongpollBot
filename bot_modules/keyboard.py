from json import encoder


RED_BUTTON = "negative"
GREEN_BUTTON = "positive"
BLUE_BUTTON = "primary"
WHITE_BUTTON = "secondary"


class Keyboard:

    def __init__(self, one_time=False, inline=False):
        self.one_time = one_time
        self.inline = inline
        self.buttons = []
        self.selected_line = 0

    # Добавить обычную кнопку
    def add_simple_button(self, label: str, color: str = "secondary", payload=None):
        if payload is None:
            payload = {}

        button = {
            'action': {
                'type': "text",
                'label': label,
                'payload': encoder.JSONEncoder().encode(payload),
            },
            'color': color,
        }

        if len(self.buttons) == self.selected_line:
            self.buttons.append([button])
        else:
            self.buttons[self.selected_line].append(button)

    # Перейти на следущую стоку клавиатуры
    def next_line(self):
        if len(self.buttons) == self.selected_line:
            return
        self.selected_line += 1

    # Сгенерировать JSON код клавиатуры
    def generate(self) -> str:
        return encoder.JSONEncoder().encode({
            'inline': self.inline,
            'one_time': self.one_time,
            'buttons': self.buttons,
        })
