import requests
import threading


class HttpClient:

    @staticmethod
    def request_task(url, json):
        requests.post(url, data=json)

    @staticmethod
    def fire_and_forget(json):
        threading.Thread(target=HttpClient.request_task,
                         args=("https://taxman.free.beeceptor.com/log-tax", json)).start()
