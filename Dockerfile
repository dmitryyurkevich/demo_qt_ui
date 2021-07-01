FROM python:3.8-slim-buster
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ecdis_ui.py qt_webdriver.py conftest.py stream_webdriver.py ./
COPY tests/test_ecdis_alive.py tests/tests_smoke.py ./tests/

COPY allure-2.6.0.tgz ./

RUN tar -zxvf allure-2.6.0.tgz -C /opt/ &&\
    ln -s /opt/allure-2.6.0/bin/allure /usr/bin/allure
    
RUN mkdir ./allure_report

ENTRYPOINT pytest --alluredir=./allure_report ./tests/tests_smoke.py

