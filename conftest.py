# -*- coding: utf-8 -*-

import os
import pytest

from selenium import webdriver

from ecdis_ui import EcdisUI
from qt_webdriver_wrapper import QtWebDriverWrapper
from stream_webdriver_wrapper import StreamWebDriver

DEFAULT_QT_WEB_DRIVER_HOST = "127.0.0.1"
DEFAULT_QT_WEB_DRIVER_PORT = 9517


@pytest.fixture(scope="session")
def ecdis_ui():
    host = os.environ.get("QT_WEB_DRIVER_HOST") or DEFAULT_QT_WEB_DRIVER_HOST
    port = os.environ.get("QT_WEB_DRIVER_PORT") or DEFAULT_QT_WEB_DRIVER_PORT

    with QtWebDriverWrapper(host=host, port=port) as qt_driver_wrapper:
        yield EcdisUI(qt_driver_wrapper=qt_driver_wrapper)


DEFAULT_QT_STREAM_HOST = "127.0.0.1"
DEFAULT_QT_STREAM_PORT = 10000
DEFAULT_QT_STREAM_PASS = "111"


@pytest.fixture(scope="session")
def ecdis_ui_stream():
    host = os.environ.get("QT_STREAM_HOST") or DEFAULT_QT_STREAM_HOST
    port = os.environ.get("QT_STREAM_PORT") or DEFAULT_QT_STREAM_PORT
    password = os.environ.get("QT_STREAM_PASS") or DEFAULT_QT_STREAM_PASS

    with StreamWebDriver(host=host, port=port, password=password) as ecdis_ui_stream:
        yield ecdis_ui_stream
