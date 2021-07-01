# -*- coding: utf-8 -*-
import numpy

from bs4 import BeautifulSoup
from collections import namedtuple
from collections.abc import Iterable
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from time import sleep

from selenium.webdriver.chrome.options import Options
from validators import url as url_validator
import os

import ecdis_ui

DELAY = 0.5

ControlProperties = namedtuple("ControlProperties", ("id", "external_id", "displayed_text",))


class QtWebDriverWrapper:
    def __init__(self, host, port):
        self.qt_driver = run_qt_driver(host=host, port=port)

        self.qt_controls = self._collect_identified_controls()
        self.qt_controls = self._collect_unidentified_controls(controls=self.qt_controls)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.qt_driver.close()


    @property
    def window_size(self):
        return self.qt_driver.get_window_size()

    @property
    def window_position(self):
        return self.qt_driver.get_window_position()

    @property
    def controls_with_external_id(self):
        return (qtc for qtc in self.qt_controls if self.qt_controls[qtc].external_id)

    @property
    def controls_with_displayed_text(self):
        return (qtc for qtc in self.qt_controls if self.qt_controls[qtc].displayed_text)

    @property
    def central_point(self):
        x = int(self.window_position["x"]) + int(self.window_size["width"] / 2)
        y = int(self.window_position["y"]) + int(self.window_size["height"] / 2)
        return x, y

    def click_on_position(self, x, y):
        assert not x > self.window_size["width"]
        assert not y > self.window_size["height"]

        ac = ActionChains(self.qt_driver)
        ac.move_to_element_with_offset(self.qt_driver.find_element_by_tag_name("Rectangle"), 0, 0)
        ac.move_by_offset(x, y).click().perform()

    def click_on_central_point(self):
        self.click_on_position(*self.central_point)

    # =============================================================================================================== #

    def _collect_identified_controls(self, controls=None):
        controls = controls or dict()

        html_tags = BeautifulSoup(self.qt_driver.page_source, 'html.parser').findAll()
        for html_tag in html_tags:
            control_external_id = html_tag.get("id")
            if control_external_id:
                artificial_ids = ("mousearea", "tabbar", "tabrow",)
                if control_external_id not in artificial_ids:
                    control = self.qt_driver.find_element_by_id(control_external_id)
                    if control:
                        if control in controls:
                            controls[control].external_id = control_external_id
                        else:
                            control_properties = ControlProperties(id=control.id, external_id=control_external_id,
                                                                   displayed_text=None)
                            controls[control] = control_properties
        return controls

    def _wake_up_sleeping_controls(self):
        xpath_controls = self.qt_driver.find_elements_by_xpath("//*[not(*)]")
        for control in xpath_controls:
            if control.text in ("Карта", "Предв. прокл.", "Основ. задачи", "Спец. задачи", "Серв. задачи", "Настройки"):
                control.click()
                sleep(DELAY)
                control.click()
                sleep(DELAY)

    def get_right_sliding_panels_offset(self):
        r_sliding_panel = self.qt_driver.find_element_by_id("TempSlidingPanel")
        assert (r_sliding_panel is not None)
        assert (r_sliding_panel.is_enabled())
        assert (r_sliding_panel.is_displayed())

        self.qt_driver.save_screenshot('screenshot_before_slide.png')

        r_sliding_panel.click()
        sleep(DELAY)
        self.qt_driver.save_screenshot('screenshot_after_slide.png')

        with Image.open("screenshot_before_slide.png") as screenshot_before:
            with Image.open("screenshot_after_slide.png") as screenshot_after:
                scr_before_sliding_array = numpy.asarray(screenshot_before)
                scr_after_sliding_array = numpy.asarray(screenshot_after)

                y = r_sliding_panel.location["y"] + r_sliding_panel.size["height"] // 2
                x = 0
                for i in range(len(scr_before_sliding_array[y - 1])):
                    if tuple(scr_before_sliding_array[y - 1, i]) != tuple(scr_after_sliding_array[y - 1, i]):
                        x = i + 1
                        break

                self.click_on_position(x=x, y=y)
                sleep(DELAY)

                self.qt_driver.save_screenshot('screenshot_final.png')
                with Image.open("screenshot_final.png") as screenshot_final:
                    scr_final_array = numpy.asarray(screenshot_final)

                    for i in range(len(scr_before_sliding_array[y - 1])):
                        if tuple(scr_before_sliding_array[y - 1, i]) != tuple(scr_final_array[y - 1, i]):
                            raise RuntimeError("something wet wrong while calculating the right panels offset")
        return x

    def _collect_unidentified_controls(self, controls=None):
        self._wake_up_sleeping_controls()
        controls = controls or dict()
        xpath_controls = self.qt_driver.find_elements_by_xpath("//*[not(*)]")
        for control in xpath_controls:
            if control in controls:
                controls[control].displayed_text = control.text
            else:
                control_properties = ControlProperties(id=control.id, external_id=None, displayed_text=control.text)
                controls[control] = control_properties

        return controls

    def find_by_displayed_text(self, displayed_text):
        if isinstance(displayed_text, str):
            for control in self.qt_controls:
                if displayed_text == control.text:
                    return control

        elif isinstance(displayed_text, Iterable):
            for possible_displayed_text in displayed_text:
                self.find_by_displayed_text(possible_displayed_text)

        raise RuntimeError(f"No control with text: {displayed_text}")

    def find_by_external_id(self, external_id):
        for control in self.qt_controls:
            if external_id == self.qt_controls[control].external_id:
                return control

    def click_central_point(self):
        elem = self.qt_driver.find_element_by_tag_name("Rectangle")
        ac = ActionChains(self.qt_driver)

        x, y = self.central_point
        ac.move_to_element(elem).move_by_offset(x, y).click().perform()


def run_qt_driver(host, port):
    driver_url = f"http://{host}:{port}"

    if not url_validator(driver_url):
        raise RuntimeError(f"not valid url: {driver_url}")

    print(f"set up and run the instance of qt driver on: {driver_url}")
    return webdriver.Remote(desired_capabilities=webdriver.DesiredCapabilities.CHROME,
                            command_executor=driver_url)


def is_clickable(element):
    return element.is_displayed() and element.is_enabled()


def filter_by_size(controls, size):
    return list(filter(lambda ctrl: ctrl.size == size, controls))


def filter_by_x_location(controls, x):
    return list(filter(lambda ctrl: ctrl.location["x"] == x, controls))


def filter_by_x_location_greater(controls, x):
    return list(filter(lambda ctrl: ctrl.location["x"] > x, controls))


def filter_by_x_location_less(controls, x):
    return list(filter(lambda ctrl: ctrl.location["x"] < x, controls))


def filter_by_y_location(controls, y):
    return list(filter(lambda ctrl: ctrl.location["y"] == y, controls))


def filter_by_y_location_greater(controls, y):
    return list(filter(lambda ctrl: ctrl.location["y"] > y, controls))


def filter_by_y_location_less(controls, y):
    return list(filter(lambda ctrl: ctrl.location["y"] < y, controls))


def sort_by_x_location(controls):
    return sorted(controls, key=lambda ctrl: ctrl.location["x"])


def sort_by_y_location(controls):
    return sorted(controls, key=lambda ctrl: ctrl.location["y"])


if __name__ == "__main__":
    qt = QtWebDriverWrapper('127.0.0.1', 9517)
    ecdis = ecdis_ui.EcdisUI(qt_driver_wrapper=qt)

    buttons = qt.qt_driver.find_elements_by_xpath("//Button[ancestor-or-self::*[@id="
                                                  "'EcdisWindowPlugin.RoutePlanningPanel']]")
    buttons = sort_by_x_location(buttons)

    ecdis.window_plugin_panels.route_planing_panel_tab().click()
    ecdis.route_planning_panel.control_points_tab().click()

    print(qt.qt_driver.page_source)

    for button in buttons:
        print(button.text, button.size, button.location)
