# -*- coding: utf-8 -*-
import allure
import pytest
from selenium.webdriver.common.keys import Keys
from time import sleep

DELAY = 0.5


@allure.feature("ECDIS end to end smoke")
@allure.story("ECDIS smoke")
def test_11(ecdis_ui):
    with allure.step("На панели сигнализации и управления СЭНК отображается "
                     "указатель номера и оригинального масштаба СЭНК."):
        chart_panel_button = ecdis_ui.alarm_and_control_panel.chart_panel_button()
        assert chart_panel_button.is_displayed()
        assert chart_panel_button.is_enabled()


@allure.feature("ECDIS end to end smoke")
@allure.story("ECDIS smoke")
def test_13(ecdis_ui):
    with allure.step("На панели сигнализации и управления СЭНК отображается "
                     "кнопка возврата к оригинальному маштабу СЭНК."):
        origin_scale_button = ecdis_ui.alarm_and_control_panel.origin_scale_button()
        assert origin_scale_button.is_displayed()
        assert origin_scale_button.is_enabled()


@allure.feature("ECDIS end to end smoke")
@allure.story("ECDIS smoke")
def test_14(ecdis_ui):
    with allure.step("На панели сигнализации и управления СЭНК отображается комбо-бокс нагрузки дисплея."):
        display_mode_switcher = ecdis_ui.alarm_and_control_panel.display_mode_switcher()
        assert display_mode_switcher.is_displayed()
        assert display_mode_switcher.is_enabled()


@allure.feature("ECDIS end to end smoke")
@allure.story("ECDIS smoke")
def test_15(ecdis_ui):
    with allure.step("На панели сигнализации и управления СЭНК отображается "
                     "кнопка стандартной нагрузки дисплея."):
        standard_mode_display_button = ecdis_ui.alarm_and_control_panel.standard_mode_display_button()
        assert standard_mode_display_button.is_displayed()
        # assert standard_mode_display_button.is_enabled()


@allure.feature("ECDIS end to end smoke")
@allure.story("ECDIS smoke")
def test_16(ecdis_ui):
    with allure.step("На панели сигнализации и управления СЭНК отображается комбо-бокс ориентации СЭНК."):

        for control in ecdis_ui.qt_driver_wrapper.qt_controls:
            print(control.text)

        chart_orientation_combobox = ecdis_ui.alarm_and_control_panel.chart_orientation_combobox()
        assert chart_orientation_combobox.is_displayed()
        assert chart_orientation_combobox.is_enabled()


@allure.feature("ECDIS end to end smoke")
@allure.story("ECDIS smoke")
def test_17(ecdis_ui):
    with allure.step("На панели сигнализации и управления СЭНК отображается "
                     "кнопка возврата позиции корабля в центр экрана."):
        center_to_ship_button = ecdis_ui.alarm_and_control_panel.center_to_ship_button()
        assert center_to_ship_button.is_displayed()
        assert center_to_ship_button.is_enabled()


@allure.feature("ECDIS end to end smoke")
@allure.story("ECDIS smoke")
def test_18(ecdis_ui):
    with allure.step("На панели сигнализации и управления СЭНК отображается комбо-бокс палитры интерфейса."):
        style_switcher_combobox = ecdis_ui.alarm_and_control_panel.style_switcher_combobox()
        assert style_switcher_combobox.is_displayed()
        assert style_switcher_combobox.is_enabled()


@allure.feature("ECDIS end to end smoke")
@allure.story("ECDIS smoke")
def test_19(ecdis_ui):
    with allure.step("На панели сигнализации и управления СЭНК отображается окно позиции курсора."):
        cursor_panel = ecdis_ui.alarm_and_control_panel.cursor_panel()
        assert cursor_panel.is_displayed()
        assert cursor_panel.is_enabled()


@allure.feature("ECDIS end to end smoke")
@allure.story("ECDIS smoke")
def test_20(ecdis_ui):
    with allure.step("На панели сигнализации и управления СЭНК отображается кнопка звукового сигнала АПС."):
        sound_alarm_button = ecdis_ui.alarm_and_control_panel.sound_alarm_button()
        assert sound_alarm_button.is_displayed()
        assert sound_alarm_button.is_enabled()


@allure.feature("ECDIS end to end smoke")
@allure.story("ECDIS smoke")
def test_21(ecdis_ui):
    with allure.step("На панели сигнализации и управления СЭНК отображается панель АПС."):
        alarm_panel = ecdis_ui.alarm_and_control_panel.alarm_panel()
        assert alarm_panel.is_displayed()
        assert alarm_panel.is_enabled()


@allure.feature("ECDIS end to end smoke")
@allure.story("ECDIS smoke")
def test_23__24(ecdis_ui):
    with allure.step("На панели сигнализации и управления СЭНК отображается панель АПС."):
        chart_panel_button = ecdis_ui.alarm_and_control_panel.chart_panel_button()
        assert chart_panel_button.is_displayed()
        assert chart_panel_button.is_enabled()
        
        for control in ecdis_ui.alarm_and_control_panel.chart_panel.all_controls:
            assert not control.is_displayed()

    with allure.step("При нажатии на панель АПС открывается дополнительная панель инструментов."):
        chart_panel_button.click()
        sleep(DELAY)

        for control in ecdis_ui.alarm_and_control_panel.chart_panel.all_controls:
            assert control.is_displayed()

    with allure.step("При повторном нажатии на панель АПС дополнительная панель инструментов не исчезает."):
        chart_panel_button.click()
        sleep(DELAY)

        for control in ecdis_ui.alarm_and_control_panel.chart_panel.all_controls:
            assert control.is_displayed()

    with allure.step("При клике в центр экрана дополнительная панель инструментов не исчезает."):
        ecdis_ui.qt_driver_wrapper.click_central_point()
        sleep(DELAY)

        for control in ecdis_ui.alarm_and_control_panel.chart_panel.all_controls:
            assert not control.is_displayed()


@allure.feature("ECDIS end to end smoke")
@allure.story("ECDIS smoke")
@pytest.mark.xfail(reason="wrong default state of the display mode switcher")
def test_26__32(ecdis_ui):
    with allure.step("В комбо-боксе нагрузки дисплея на панели сигнализации и управления СЭНК "
                     "установлено значение по умолчанию \"Стандартная\"."):
        display_mode_switcher = ecdis_ui.alarm_and_control_panel.display_mode_switcher()
        assert display_mode_switcher.is_displayed()
        assert display_mode_switcher.is_enabled()

        display_mode = ecdis_ui.qt_driver_wrapper.find_by_displayed_text("Стандартная")
        assert display_mode
        assert display_mode.text == "Стандартная"

    with allure.step("Кнопка \"СТД\" в статусе \"неактивна\"."):
        standard_mode_display_button = ecdis_ui.alarm_and_control_panel.standard_mode_display_button()
        assert standard_mode_display_button.is_displayed()
        assert not standard_mode_display_button.is_enabled()

    with allure.step("В комбо-боксе нагрузки дисплея устанавливаем значение \"Базовая\"."):
        display_mode_switcher.click()
        display_mode_switcher.send_keys(Keys.ARROW_UP)
        display_mode_switcher.send_keys(Keys.ENTER)

        assert display_mode.text == "Базовая"

    with allure.step("Кнопка \"СТД\" меняет статус на \"активна\"."):
        assert standard_mode_display_button.is_displayed()
        assert standard_mode_display_button.is_enabled()

    with allure.step("В комбо-боксе нагрузки дисплея устанавливаем значение \"Полная\"."):
        display_mode_switcher.click()
        display_mode_switcher.send_keys(Keys.ARROW_DOWN)
        display_mode_switcher.send_keys(Keys.ARROW_DOWN)
        display_mode_switcher.send_keys(Keys.ENTER)

        assert display_mode.text == "Полная"

    with allure.step("Кнопка \"СТД\" находится в статусе \"активна\"."):
        assert standard_mode_display_button.is_displayed()
        assert standard_mode_display_button.is_enabled()

    with allure.step("В комбо-боксе нагрузки дисплея вновь устанавливаем значение \"Базовая\"."):
        display_mode_switcher.click()
        display_mode_switcher.send_keys(Keys.ARROW_UP)
        display_mode_switcher.send_keys(Keys.ARROW_UP)
        display_mode_switcher.send_keys(Keys.ENTER)

        assert display_mode.text == "Базовая"

    with allure.step("Кнопка \"СТД\" остаётся в статусе \"активна\"."):
        assert standard_mode_display_button.is_displayed()
        assert standard_mode_display_button.is_enabled()

    with allure.step("Нажимаем на кнопку \"СТД\"."):
        standard_mode_display_button.click()
        sleep(DELAY)

    with allure.step("В комбо-боксе нагрузки дисплея устанавилось значение \"Стандартная\"."):
        assert display_mode.text == "Стандартная"
        assert standard_mode_display_button.is_displayed()
        assert not standard_mode_display_button.is_enabled()
        assert False


@allure.feature("ECDIS end to end smoke")
@allure.story("ECDIS smoke")
def test_33_36(ecdis_ui):
    with allure.step("В комбо-боксе ориентации дисплея на панели сигнализации и управления СЭНК "
                     "установлено значение по умолчанию \"По северу\"."):
        chart_orientation_combobox = ecdis_ui.alarm_and_control_panel.chart_orientation_combobox()
        assert chart_orientation_combobox.is_displayed()
        assert chart_orientation_combobox.is_enabled()

        orientation = ecdis_ui.qt_driver_wrapper.find_by_displayed_text("По северу")
        assert orientation
        assert orientation.text == "По северу"

    with allure.step("В комбо-боксе ориентации дисплея устанавливаем значение \"По ПУ\"."):
        chart_orientation_combobox.click()
        chart_orientation_combobox.send_keys(Keys.ARROW_DOWN)
        chart_orientation_combobox.send_keys(Keys.ENTER)
        assert orientation.text == "По ПУ"

    with allure.step("В комбо-боксе ориентации дисплея устанавливаем значение \"По маршруту\"."):
        chart_orientation_combobox.click()
        chart_orientation_combobox.send_keys(Keys.ARROW_DOWN)
        chart_orientation_combobox.send_keys(Keys.ENTER)
        assert orientation.text == "По маршруту"

    with allure.step("В комбо-боксе ориентации дисплея возвращаем значение \"По северу\"."):
        chart_orientation_combobox.click()
        chart_orientation_combobox.send_keys(Keys.ARROW_UP)
        chart_orientation_combobox.send_keys(Keys.ARROW_UP)
        chart_orientation_combobox.send_keys(Keys.ENTER)
        assert orientation.text == "По северу"


@allure.feature("ECDIS end to end smoke")
@allure.story("ECDIS smoke")
def test_38_41(ecdis_ui):
    with allure.step("В комбо-боксе палитры интерфейса на панели сигнализации и управления СЭНК "
                     "установлено значение по умолчанию \"День\"."):
        style_switcher_combobox = ecdis_ui.alarm_and_control_panel.style_switcher_combobox()
        assert style_switcher_combobox.is_displayed()
        assert style_switcher_combobox.is_enabled()

        style = ecdis_ui.qt_driver_wrapper.find_by_displayed_text("День")
        assert style
        assert style.text == "День"

    with allure.step("В комбо-боксе палитры интерфейса устанавливаем значение \"Сумерки\"."):
        style_switcher_combobox.click()
        style_switcher_combobox.send_keys(Keys.ARROW_DOWN)
        style_switcher_combobox.send_keys(Keys.ENTER)
        assert style.text == "Сумерки"

    with allure.step("В комбо-боксе палитры интерфейса устанавливаем значение \"Ночь\"."):
        style_switcher_combobox.click()
        style_switcher_combobox.send_keys(Keys.ARROW_DOWN)
        style_switcher_combobox.send_keys(Keys.ENTER)
        assert style.text == "Ночь"

    with allure.step("В комбо-боксе палитры интерфейса возвращаем значение \"День\"."):
        style_switcher_combobox.click()
        style_switcher_combobox.send_keys(Keys.ARROW_UP)
        style_switcher_combobox.send_keys(Keys.ARROW_UP)
        style_switcher_combobox.send_keys(Keys.ENTER)
        assert style.text == "День"


@allure.feature("ECDIS end to end smoke")
@allure.story("ECDIS smoke")
def test_46(ecdis_ui):
    with allure.step("Панель индикации времени отображается в ПО ЭКНИС."):
        time_panel_button = ecdis_ui.alarm_and_control_panel.time_panel_button()
        assert time_panel_button.is_displayed()
        assert time_panel_button.is_enabled()


@allure.feature("ECDIS end to end smoke")
@allure.story("ECDIS smoke")
def test_49(ecdis_ui):
    with allure.step("Кнопка \"Человек за бортом\" отображается в панели инструментов."):
        man_over_board_button = ecdis_ui.navigation_panel.man_over_board_button()
        assert man_over_board_button.is_displayed()
        assert man_over_board_button.is_enabled()


@allure.feature("ECDIS end to end smoke")
@allure.story("ECDIS smoke")
def test_52(ecdis_ui):
    with allure.step("Кнопка \"САРП\" отображается на панели инструментов."):
        arpa_button = ecdis_ui.navigation_panel.arpa_button()
        assert arpa_button.is_displayed()
        assert arpa_button.is_enabled()


@allure.feature("ECDIS end to end smoke")
@allure.story("ECDIS smoke")
def test_53(ecdis_ui):
    with allure.step("Кнопка \"РЛС\" отображается на панели инструментов."):
        radars_button = ecdis_ui.navigation_panel.radars_button()
        assert radars_button.is_displayed()
        assert radars_button.is_enabled()


@allure.feature("ECDIS end to end smoke")
@allure.story("ECDIS smoke")
def test_54(ecdis_ui):
    with allure.step("Кнопка \"АИС\" отображается на панели инструментов."):
        ais_button = ecdis_ui.navigation_panel.ais_button()
        assert ais_button.is_displayed()
        assert ais_button.is_enabled()


@allure.feature("ECDIS end to end smoke")
@allure.story("ECDIS smoke")
def test_56(ecdis_ui):
    with allure.step("Кнопка \"Счисление\" отображается на панели инструментов."):
        coordinates_amend_button = ecdis_ui.navigation_panel.coordinates_amend_button()
        assert coordinates_amend_button.is_displayed()
        assert coordinates_amend_button.is_enabled()


@allure.feature("ECDIS end to end smoke")
@allure.story("ECDIS smoke")
def test_61(ecdis_ui):
    with allure.step("Кнопка разделения экрана отображается на панели инструментов."):
        split_screen_button = ecdis_ui.navigation_panel.split_screen_button()
        assert split_screen_button.is_displayed()
        assert split_screen_button.is_enabled()


@allure.feature("ECDIS end to end smoke")
@allure.story("ECDIS smoke")
def test_62(ecdis_ui):
    with allure.step("Кнопка включения/выключения отображения боковых панелей отображается на панели инструментов."):
        switch_slide_bar_button = ecdis_ui.navigation_panel.switch_slide_bar_button()
        assert switch_slide_bar_button.is_displayed()
        assert switch_slide_bar_button.is_enabled()


@allure.feature("ECDIS end to end smoke")
@allure.story("ECDIS smoke")
def test_63(ecdis_ui):
    with allure.step("Кнопка включения/выключения панели задач отображается на панели инструментов."):
        switch_bottom_panel_button = ecdis_ui.navigation_panel.switch_bottom_panel_button()
        assert switch_bottom_panel_button.is_displayed()
        assert switch_bottom_panel_button.is_enabled()


@allure.feature("ECDIS end to end smoke")
@allure.story("ECDIS smoke")
def test_64(ecdis_ui):
    with allure.step("Кнопка очистки экрана отображается на панели инструментов."):
        hide_al_button = ecdis_ui.navigation_panel.hide_al_button()
        assert hide_al_button.is_displayed()
        assert hide_al_button.is_enabled()


@allure.feature("ECDIS end to end smoke")
@allure.story("ECDIS smoke")
def test_85(ecdis_ui):
    with allure.step("Таб \"Карта\" отображается на панели задач."):
        maps_panel_tab = ecdis_ui.window_plugin_panels.maps_panel_tab()
        assert maps_panel_tab.is_displayed()
        assert maps_panel_tab.is_enabled()


@allure.feature("ECDIS end to end smoke")
@allure.story("ECDIS smoke")
def test_86(ecdis_ui):
    with allure.step("Таб \"Предв. прокл.\" отображается на панели задач."):
        maps_panel_tab = ecdis_ui.window_plugin_panels.route_planing_panel_tab()
        assert maps_panel_tab.is_displayed()
        assert maps_panel_tab.is_enabled()


@allure.feature("ECDIS end to end smoke")
@allure.story("ECDIS smoke")
def test_87(ecdis_ui):
    with allure.step("Таб \"Основ. задачи\" отображается на панели задач."):
        maps_panel_tab = ecdis_ui.window_plugin_panels.main_tasks_panel_tab()
        assert maps_panel_tab.is_displayed()
        assert maps_panel_tab.is_enabled()


@allure.feature("ECDIS end to end smoke")
@allure.story("ECDIS smoke")
def test_88(ecdis_ui):
    with allure.step("Таб \"Спец. задачи\" отображается на панели задач."):
        maps_panel_tab = ecdis_ui.window_plugin_panels.special_tasks_panel_tab()
        assert maps_panel_tab.is_displayed()
        assert maps_panel_tab.is_enabled()


@allure.feature("ECDIS end to end smoke")
@allure.story("ECDIS smoke")
def test_89(ecdis_ui):
    with allure.step("Таб \"Серв. задачи\" отображается на панели задач."):
        maps_panel_tab = ecdis_ui.window_plugin_panels.service_tasks_panel_tab()
        assert maps_panel_tab.is_displayed()
        assert maps_panel_tab.is_enabled()


@allure.feature("ECDIS end to end smoke")
@allure.story("ECDIS smoke")
def test_90(ecdis_ui):
    with allure.step("Таб \"Настройки\" отображается на панели задач."):
        maps_panel_tab = ecdis_ui.window_plugin_panels.settings_panel_tab()
        assert maps_panel_tab.is_displayed()
        assert maps_panel_tab.is_enabled()


@allure.feature("ECDIS end to end smoke")
@allure.story("ECDIS smoke")
def test_91__93(ecdis_ui):
    maps_panel_tab = ecdis_ui.window_plugin_panels.maps_panel_tab()
    settings_panel_tab = ecdis_ui.window_plugin_panels.settings_panel_tab()

    with allure.step("Панель \"Карта\" закрыта и не отображается на дисплее."):
        settings_panel_tab.click()

        for control in ecdis_ui.window_plugin_panels.maps_panel.all_controls:
            assert not control.is_displayed()

    with allure.step("Панель \"Карта\" открывается при нажатии."):
        maps_panel_tab.click()

        for control in ecdis_ui.window_plugin_panels.maps_panel.all_controls:
            assert control.is_displayed()

    with allure.step("Панель \"Карта\" закрывается при нажатии."):
        settings_panel_tab.click()

        for control in ecdis_ui.window_plugin_panels.maps_panel.all_controls:
            assert not control.is_displayed()


@allure.feature("ECDIS end to end smoke")
@allure.story("ECDIS smoke")
def test_100__101(ecdis_ui):
    special_tasks_panel_tab = ecdis_ui.window_plugin_panels.special_tasks_panel_tab()
    maps_panel_tab = ecdis_ui.window_plugin_panels.maps_panel_tab()

    with allure.step("Панель \"Спец. задачи\" закрыта и не отображается на дисплее."):
        maps_panel_tab.click()
        sleep(0.2)

        for control in ecdis_ui.window_plugin_panels.special_tasks_panel.all_controls:
            assert not control.is_displayed()

    with allure.step("Панель \"Спец. задачи\" открывается при нажатии."):
        special_tasks_panel_tab.click()
        sleep(0.2)

        for control in ecdis_ui.window_plugin_panels.special_tasks_panel.all_controls:
            assert control.is_displayed()

    with allure.step("Панель \"Спец. задачи\" закрывается при нажатии."):
        maps_panel_tab.click()
        sleep(0.2)

        for control in ecdis_ui.window_plugin_panels.special_tasks_panel.all_controls:
            assert not control.is_displayed()


@allure.feature("ECDIS end to end smoke")
@allure.story("ECDIS smoke")
def test_102__103(ecdis_ui):
    service_tasks_panel_tab = ecdis_ui.window_plugin_panels.service_tasks_panel_tab()
    maps_panel_tab = ecdis_ui.window_plugin_panels.maps_panel_tab()

    with allure.step("Панель \"Серв. задачи\" закрыта и не отображается на дисплее."):
        maps_panel_tab.click()
        sleep(0.2)

        for control in ecdis_ui.window_plugin_panels.service_tasks_panel.all_controls:
            assert not control.is_displayed()

    with allure.step("Панель \"Серв. задачи\" открывается при нажатии."):
        service_tasks_panel_tab.click()
        sleep(0.2)

        for control in ecdis_ui.window_plugin_panels.service_tasks_panel.all_controls:
            assert control.is_displayed()

    with allure.step("Панель \"Серв. задачи\" закрывается при нажатии."):
        maps_panel_tab.click()
        sleep(0.2)

        for control in ecdis_ui.window_plugin_panels.service_tasks_panel.all_controls:
            assert not control.is_displayed()


