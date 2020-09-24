import requests


class Bot:

    def __init__(self, token: str, group_id: int):
        self.server = self.ts = self.key = ""
        self.token = token
        self.group_id = group_id

    # Обновить данные для подключения к longpoll
    def update_longpoll(self):
        response = self.send_request("groups.getLongPollServer", {
            'group_id': self.group_id
        })['response']

        self.server = response['server']
        self.key = response['key']
        self.ts = response['ts']

    # Старт бота
    def start(self):
        self.update_longpoll()

        while True:
            print(self.get_longpoll_data())

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
