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

    # Добавить кнопку в список кнопок
    def add_button_to_list(self, button: dict):
        if len(self.buttons) == self.selected_line:
            self.buttons.append([button])
        else:
            self.buttons[self.selected_line].append(button)

    # Добавить обычную кнопку
    def add_text_button(self, label: str, color: str = "secondary", payload=None):
        if payload is None:
            payload = {}

        self.add_button_to_list({
            'action': {
                'type': "text",
                'label': label,
                'payload': encoder.JSONEncoder().encode(payload),
            },
            'color': color,
        })

    # Добавить кнопку с ссылкой
    def add_open_link_button(self, label: str, url: str = "https://vk.com"):
        self.add_button_to_list({
            'action': {
                'type': "open_link",
                'link': url,
                'label': label,
                'payload': "{}",
            }
        })

    # Добавить кнопку с VK Pay
    def add_vk_pay_button(self, payload=None, pay_hash: str = ""):
        if payload is None:
            payload = {}

        self.add_button_to_list({
            'action': {
                'type': "vkpay",
                'payload': encoder.JSONEncoder().encode(payload),
                'hash': pay_hash,
            }
        })

    # Добавить CallBack кнопку
    def add_callback_button(self, title: str = "", payload=None):
        if payload is None:
            payload = {}

        self.add_button_to_list({
            'action': {
                'type': "callback",
                'title': title,
                'payload': encoder.JSONEncoder().encode(payload),
            }
        })

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
