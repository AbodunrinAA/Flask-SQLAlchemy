import requests
import threading


class HttpClient:
    def __init__(self):
        self.url = "https://taxman.free.beeceptor.com/log-tax"

    @staticmethod
    def request_task(url, json, headers):
        requests.post(url, data=json, headers=headers)

    @staticmethod
    def fire_and_forget(url, json, headers):
        threading.Thread(target=HttpClient.request_task, args=(url, json, headers)).start()
