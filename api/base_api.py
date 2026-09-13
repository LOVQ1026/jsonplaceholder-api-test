import requests
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class BaseApi:
    def __init__(self, base_url="https://jsonplaceholder.typicode.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def send(self, method, path, **kwargs):
        url = self.base_url + path
        logging.info(f"请求: {method.upper()} {url} | 参数: {kwargs}")
        response = self.session.request(method, url, **kwargs)
        logging.info(f"响应: {response.status_code} | {response.text[:150]}")
        return response