import requests
import asyncio
import bot_exceptions as ex


class Bot:
    enabled = True

    def __init__(self, token: str, group_id: int):
        self.server = self.ts = self.key = ""
        self.token = token
        self.group_id = group_id

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

    # Ассинхронный метод в котором производить какие-то действия
    async def action(self, event_type: str, data: dict, event_id: str):
        # TODO...
        pass
