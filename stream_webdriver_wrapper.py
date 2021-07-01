# -*- coding: utf-8 -*-

from selenium import webdriver
from validators import url as url_validator
from time import sleep

DEFAULT_QT_STREAM_HOST = "127.0.0.1"
DEFAULT_QT_STREAM_PORT = 10000
DEFAULT_QT_STREAM_PASS = "111"


class StreamWebDriver:
    __slots__ = "stream_driver"

    def __init__(self, host, port, password):
        self.stream_driver = run_stream_driver(host=host, port=port, password=password)

    def __enter__(self):
        return self.stream_driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stream_driver.close()

    def get_screenshot(self, file_path):
        self.stream_driver.save_screenshot(file_path)


def run_stream_driver(host, port, password):
    stream_driver = webdriver.Chrome(executable_path="./chromedriver")

    # TO DO: maybe this can be parameterized
    stream_driver.set_window_position(0, 0)
    stream_driver.set_window_size(1920, 1080)

    stream_url = f"http://{host}:{port}/index.html?encoding=rgb32&password={password}"
    print(f"attach to the application web stream on on: {stream_url}")

    if not url_validator(stream_url):
        raise RuntimeError(f"not valid url: {stream_url}")

    print(f"attach to the application web stream on on: {stream_url}")
    stream_driver.get(stream_url)

    wait_stream_started(stream_driver)
    return stream_driver


# TO DO: improve this wait method
def wait_stream_started(stream_driver):
    sleep(2)
    return True
