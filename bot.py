import requests
import asyncio
import bot_exceptions as ex


class Bot:
    enabled = True

    def __init__(self, token: str, group_id: int):
        self.server = self.ts = self.key = ""
        self.token = token
        self.group_id = group_id
        self.messages = MessagesMethods(self)
        self.event_listener = EventListener()

    # Обновить данные для подключения к longpoll
    def update_longpoll(self):
        response = self.send_request("groups.getLongPollServer", {
            'group_id': self.group_id
        })

        if "error" in response:
            raise ex.AuthFail
        response = response["response"]

        self.server = response['server']
        self.key = response['key']
        self.ts = response['ts']

    def start(self):
        self.update_longpoll()

        while self.enabled:
            updates = self.get_longpoll_data()['updates']
            if not updates:
                continue

            for update in updates:
                asyncio.run(self.action(
                    update['type'],
                    update['object'],
                    update['event_id']
                ))

    # Отправка запороса к api серверу
    def send_request(self, method: str, params: dict) -> dict:
        params['access_token'] = self.token
        params['v'] = "5.124"

        return requests.post("https://api.vk.com/method/" + method, params).json()

    # Получение данных из longpoll сервера
    def get_longpoll_data(self) -> dict:
        while True:
            request = requests.post(f"{self.server}?act=a_check&key={self.key}&ts={self.ts}&wait=25").json()

            if "failed" not in request:
                break

            if request['failed'] == 1:
                self.ts = int(request['ts'])
                continue

            self.update_longpoll()
        self.ts = request['ts']
        return request

    # В данном методе обрабатываются различные события
    async def action(self, event_type: str, data: dict, event_id: str):
        self.event_listener.execute(event_type, data, event_id)


# Проверка: является ли peer_id чатом?
def is_peer_id_own_by_chat(peer_id) -> bool:
    return 2000000000 < peer_id


# Получение прикрепленных сообщений
def get_reply_messages(message_object: dict) -> list:
    lst = list()
    if "fwd_messages" in message_object:
        lst += message_object['fwd_messages']
    if "reply_message" in message_object:
        lst.append(message_object['reply_message'])
    return lst


class EventListener(object):

    def __init__(self):
        self.listeners = {}

    # Обработать события
    def execute(self, event_type: str, data: dict, event_id: str):
        if event_type not in self.listeners:
            return

        for method in self.listeners[event_type]:
            method(data, event_id)


# Добавиляет метод в обработчик событий
def add_method_to_listener(listeners: dict, event_type: str):
    def add_to_listener_list(func):
        if event_type not in listeners:
            listeners[event_type] = []
        listeners[event_type].append(func)

        def execute():
            print("c")
            func()
        return execute
    return add_to_listener_list


class MessagesMethods:

    def __init__(self, bot: Bot):
        self.bot = bot

    # Отправка сообщения
    def messages_send(self,
                      peer_id: int,
                      message: str = "",
                      attachment: str = None,
                      keyboard: str = None,
                      dont_parse_links: bool = False
                      ) -> dict:
        params = {
            'random_id': 0,
            'peer_id': peer_id,
            'message': message,
            'dont_parse_links': dont_parse_links
        }

        if attachment is not None:
            params['attachment'] = attachment
        if keyboard is not None:
            params['keyboard'] = keyboard

        return self.bot.send_request("messages.send", params)

    # Удаляет пользователя из чата
    def remove_user_from_chat(self, chat_id: int, target: int):
        if is_peer_id_own_by_chat(chat_id):
            chat_id -= 2000000000

        self.bot.send_request("messages.removeChatUser", {
            'chat_id': chat_id,
            'user_id': target,
        })
