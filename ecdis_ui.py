# -*- coding: utf-8 -*-
import functools

import qt_webdriver_wrapper
from qt_webdriver_wrapper import filter_by_size
from qt_webdriver_wrapper import filter_by_x_location, sort_by_y_location
from qt_webdriver_wrapper import filter_by_y_location_greater, filter_by_y_location_less


class EcdisUI:
    def __init__(self, qt_driver_wrapper):
        self.qt_driver_wrapper = qt_driver_wrapper

        self.alarm_and_control_panel = AlarmAndControlPanel(qt_driver_wrapper=self.qt_driver_wrapper)
        self.navigation_panel = NavigationPanel(qt_driver_wrapper=self.qt_driver_wrapper)
        self.window_plugin_panels = WindowPluginPanels(qt_driver_wrapper=self.qt_driver_wrapper)
        self.route_planning_panel = RoutePlaningPanel(qt_driver_wrapper=self.qt_driver_wrapper)


def cached(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        cached_result = self.cache.get(method.__name__)
        if not cached_result:
            result = method(self, *args, **kwargs)
            if result:
                self.cache[method.__name__] = result
            return result
        return cached_result

    return wrapper


class EcdisControls:
    __slots__ = ("qt_driver_wrapper", "cache",)

    def __init__(self, qt_driver_wrapper):
        self.qt_driver_wrapper = qt_driver_wrapper
        self.cache = dict()


class AlarmAndControlPanel(EcdisControls):
    def __init__(self, qt_driver_wrapper):
        super().__init__(qt_driver_wrapper)
        self.chart_panel = ChartPanel(qt_driver_wrapper=self.qt_driver_wrapper)

    @cached
    def chart_panel_button(self):
        return self.qt_driver_wrapper.find_by_external_id("chartPanelButton")

    @cached
    def origin_scale_button(self):
        return self.qt_driver_wrapper.find_by_external_id("originScaleButton") or \
               self.qt_driver_wrapper.find_by_displayed_text("1:1")

    @cached
    def display_mode_switcher(self):
        return self.qt_driver_wrapper.find_by_external_id("displayModeSwitcher")

    @cached
    def standard_mode_display_button(self):
        return self.qt_driver_wrapper.find_by_external_id("standardDisplayModeButton") or \
               self.qt_driver_wrapper.find_by_displayed_text("СТД")

    @cached
    def chart_orientation_combobox(self):
        return self.qt_driver_wrapper.find_by_external_id("chartOrientationComboBox") or \
               self.qt_driver_wrapper.find_by_displayed_text("По северу")

    @cached
    def center_to_ship_button(self):
        return self.qt_driver_wrapper.find_by_external_id("centerToShipButton")

    @cached
    def style_switcher_combobox(self):
        return self.qt_driver_wrapper.find_by_external_id("styleSwitcherComboBox") or \
               self.qt_driver_wrapper.find_by_displayed_text(("День", "Сумерки", "Ночь",))

    @cached
    def cursor_panel(self):
        return self.qt_driver_wrapper.find_by_external_id("cursorPanel")

    @cached
    def sound_alarm_button(self):
        return self.qt_driver_wrapper.find_by_external_id("soundAlarmButton")

    @cached
    def alarm_panel(self):
        return self.qt_driver_wrapper.find_by_external_id("alarmPanel")

    @cached
    def warning_panel(self):
        return self.qt_driver_wrapper.find_by_external_id("warningPanel")

    @cached
    def warning_table(self):
        return self.qt_driver_wrapper.find_by_external_id("warningTable")

    @cached
    def alarm_table(self):
        return self.qt_driver_wrapper.find_by_external_id("alarmTable")

    @cached
    def information_table(self):
        return self.qt_driver_wrapper.find_by_external_id("informationTable")

    @cached
    def time_panel_button(self):
        return self.qt_driver_wrapper.find_by_external_id("timePanelButton")


class ChartPanel(EcdisControls):

    @cached
    def charts_button(self):
        return self.qt_driver_wrapper.find_by_external_id("chartPopupChartButton") or \
               self.qt_driver_wrapper.find_by_displayed_text("Карты")

    @cached
    def scale_button(self):
        return self.qt_driver_wrapper.find_by_external_id("chartPopupScaleButton") or \
               self.qt_driver_wrapper.find_by_displayed_text("Масштаб")

    @cached
    def wsg_84_button(self):
        return self.qt_driver_wrapper.find_by_external_id("chartPopupCoordButton") or \
               self.qt_driver_wrapper.find_by_displayed_text("WSG 84")

    @cached
    def zoom_area_in_button(self):
        return self.qt_driver_wrapper.find_by_external_id("zoomAreaZoomInButton")

    @cached
    def zoom_area_out_button(self):
        return self.qt_driver_wrapper.find_by_external_id("zoomAreaZoomOutButton")

    @cached
    def back_button(self):
        return self.qt_driver_wrapper.find_by_external_id("chartPopupBackButton")

    @property
    def all_controls(self):
        yield self.charts_button()
        yield self.scale_button()
        yield self.wsg_84_button()
        yield self.zoom_area_in_button()
        yield self.zoom_area_out_button()
        yield self.back_button()


class WindowPluginPanels(EcdisControls):
    def __init__(self, qt_driver_wrapper):
        super().__init__(qt_driver_wrapper)

        self.maps_panel = MapsPanel(qt_driver_wrapper=self.qt_driver_wrapper)
        self.route_planning_panel = RoutePlaningPanel(qt_driver_wrapper=self.qt_driver_wrapper)
        self.main_tasks_panel = MainTasksPanel(qt_driver_wrapper=self.qt_driver_wrapper)
        self.special_tasks_panel = SpecialTasksPanel(qt_driver_wrapper=self.qt_driver_wrapper)
        self.service_tasks_panel = ServiceTasksPanel(qt_driver_wrapper=self.qt_driver_wrapper)
        self.settings_panel = SettingsPanel(qt_driver_wrapper=self.qt_driver_wrapper)

    @cached
    def maps_panel_tab(self):
        # return self.qt_driver_wrapper.find_by_external_id("EcdisWindowPlugin.MapPanel") or \
        #        self.qt_driver_wrapper.find_by_displayed_text("Карта")
        return self.qt_driver_wrapper.find_by_displayed_text("Карта")

    @cached
    def route_planing_panel_tab(self):
        # return self.qt_driver_wrapper.find_by_external_id("EcdisWindowPlugin.RoutePlanningPanel") or \
        #        self.qt_driver_wrapper.find_by_displayed_text("Предв. прокл.")
        return self.qt_driver_wrapper.find_by_displayed_text("Предв. прокл.")

    @cached
    def main_tasks_panel_tab(self):
        return self.qt_driver_wrapper.find_by_external_id("EcdisWindowPlugin.MainTasksPanel") or \
               self.qt_driver_wrapper.find_by_displayed_text("Основ. задачи")

    @cached
    def special_tasks_panel_tab(self):
        # return self.qt_driver_wrapper.find_by_external_id("EcdisWindowPlugin.SpecialTasksPanel") or \
        return self.qt_driver_wrapper.find_by_displayed_text("Спец. задачи")

    @cached
    def service_tasks_panel_tab(self):
        # return self.qt_driver_wrapper.find_by_external_id("EcdisWindowPlugin.ServiceTasksPanel") or \
        return self.qt_driver_wrapper.find_by_displayed_text("Серв. задачи")

    @cached
    def settings_panel_tab(self):
        # return self.qt_driver_wrapper.find_by_external_id("EcdisWindowPlugin.SettingsPanel") or \
        return self.qt_driver_wrapper.find_by_displayed_text("Настройки")

    @property
    def all_controls(self):
        yield self.maps_panel_tab()
        yield self.route_planing_panel_tab()
        yield self.main_tasks_panel_tab()
        yield self.special_tasks_panel_tab()
        yield self.service_tasks_panel_tab()
        yield self.service_tasks_panel_tab()
        yield self.settings_panel_tab()


class MapsPanel(EcdisControls):
    def __init__(self, qt_driver_wrapper):
        super().__init__(qt_driver_wrapper)

        self.maps_collection_panel = MapsCollectionPanel(qt_driver_wrapper=self.qt_driver_wrapper)
        self.proofreading_panel = ProofreadingPanel(qt_driver_wrapper=self.qt_driver_wrapper)
        self.proofreading_panel = CustomLayersPanel(qt_driver_wrapper=self.qt_driver_wrapper)
        self.ecc_settings_panel = CustomLayersPanel(qt_driver_wrapper=self.qt_driver_wrapper)

    @cached
    def maps_collection_tab(self):
        return self.qt_driver_wrapper.find_by_displayed_text("Коллекция карт")

    @cached
    def proofreading_tab(self):
        return self.qt_driver_wrapper.find_by_displayed_text("Корректура")

    @cached
    def custom_layers_tab(self):
        return self.qt_driver_wrapper.find_by_displayed_text("Пользовательские слои")

    @cached
    def ecc_settings_tab(self):
        return self.qt_driver_wrapper.find_by_displayed_text("Настройка ЭНК")

    @property
    def all_controls(self):
        yield self.maps_collection_tab()
        yield self.proofreading_tab()
        yield self.custom_layers_tab()
        yield self.ecc_settings_tab()


class MapsCollectionPanel(EcdisControls):
    pass


class ProofreadingPanel(EcdisControls):
    pass


class CustomLayersPanel(EcdisControls):
    pass


class EccSettingsPanel(EcdisControls):
    pass


class RoutePlaningPanel(EcdisControls):
    """
    Page_Object - предварительная прокладка маршрута
    """

    @cached
    def all_route_planning_buttons(self):
        """

        :return: WebElements Все кнопки раздела "Прокладка маршрута"
        """
        section_btns = self.qt_driver_wrapper.qt_driver.find_elements_by_xpath("//Button[ancestor-or-self::*[@id="
                                                                               "'EcdisWindowPlugin.RoutePlanningPanel']]")
        return qt_webdriver_wrapper.sort_by_x_location(section_btns)

    @cached
    def route_points_tab(self):
        """

        :return: WebElement "Вкладка Путевые точки"
        """
        return self.qt_driver_wrapper.find_by_displayed_text("Путевые точки")

    @cached
    def hide_route_list_button(self):
        """
        :return: WebElement "Кнопка скрыть Коллекцию маршрутов"
        """

        return self.all_route_planning_buttons()[0]

    @cached
    def add_new_route_button(self):
        """
        :return: WebElement "Кнопка создания маршрута"
        """
        return self.all_route_planning_buttons()[1]

    @cached
    def delete_route_button(self):
        return self.all_route_planning_buttons()[8]

    @cached
    def apply_route_name_button(self):
        return self.all_route_planning_buttons()[-4]

    @cached
    def cancel_route_name_button(self):
        return self.all_route_planning_buttons()[-3]

    @cached
    def modify_route_button(self):
        return self.all_route_planning_buttons()[10]

    @cached
    def add_route_point_button(self):
        return self.all_route_planning_buttons()[11]

    @cached
    def cancel_changes_button(self):
        return self.all_route_planning_buttons()[12]

    @cached
    def delete_route_point_button(self):
        return self.all_route_planning_buttons()[13]

    @cached
    def save_route_button(self):
        return self.all_route_planning_buttons()[14]

    @cached
    def route_schedule_tab(self):
        return self.qt_driver_wrapper.find_by_displayed_text("Расписание")

    @cached
    def reference_points_tab(self):
        return self.qt_driver_wrapper.find_by_displayed_text("Ориентиры")

    @cached
    def navigation_calc_tab(self):
        return self.qt_driver_wrapper.find_by_displayed_text("Навигац. расчеты")

    @cached
    def control_points_tab(self):
        route_planning_controls = self.qt_driver_wrapper.qt_driver.find_elements_by_xpath(
            "//*[not(*) and ancestor-or-self::*[@id="
            "'EcdisWindowPlugin.RoutePlanningPanel']]")
        return [control for control in route_planning_controls if control.text == 'Контрольные\nточки'][1] \
               or self.qt_driver_wrapper.find_by_displayed_text("Контрольные\nточки")

    @cached
    def on_the_road_btn(self):
        return self.qt_driver_wrapper.find_by_displayed_text("В путь!")

    @cached
    def security_check_tab(self):
        return self.qt_driver_wrapper.find_by_displayed_text("Проверка на безопасность")


class MainTasksPanel(EcdisControls):
    pass


class SpecialTasksPanel(EcdisControls):
    @cached
    def observation_button(self):
        return self.qt_driver_wrapper.find_by_displayed_text("Обсервация")

    @cached
    def astronomy_button(self):
        return self.qt_driver_wrapper.find_by_displayed_text("Астрономия")

    @cached
    def sme_determination_button(self):
        return self.qt_driver_wrapper.find_by_displayed_text("Определение МЭК")

    @cached
    def navigation_tactics_button(self):
        return self.qt_driver_wrapper.find_by_displayed_text("Нав-тактика")

    @cached
    def anchorage_button(self):
        return self.qt_driver_wrapper.find_by_displayed_text("Якорная стоянка")

    @cached
    def search_and_rescue_button(self):
        return self.qt_driver_wrapper.find_by_displayed_text("Поиск и спасение")

    @cached
    def geodetic_calculations_button(self):
        return self.qt_driver_wrapper.find_by_displayed_text("Геодезические вычисления")

    @cached
    def route_along_the_track_button(self):
        return self.qt_driver_wrapper.find_by_displayed_text("Маршрут по треку")

    @property
    def all_controls(self):
        yield self.observation_button()
        yield self.astronomy_button()
        yield self.sme_determination_button()
        yield self.navigation_tactics_button()
        yield self.anchorage_button()
        yield self.search_and_rescue_button()
        yield self.geodetic_calculations_button()
        yield self.route_along_the_track_button()


class ServiceTasksPanel(EcdisControls):
    @cached
    def ais_messages_button(self):
        return self.qt_driver_wrapper.find_by_displayed_text("Сообщения АИС")

    @cached
    def navtex_messages_button(self):
        return self.qt_driver_wrapper.find_by_displayed_text("Сообщения NAVTEX")

    @cached
    def web_services_button(self):
        return self.qt_driver_wrapper.find_by_displayed_text("Веб-сервисы")

    @property
    def all_controls(self):
        yield self.ais_messages_button()
        yield self.navtex_messages_button()
        yield self.web_services_button()


class SettingsPanel(EcdisControls):
    @cached
    def system_panel_tab(self):
        return self.qt_driver_wrapper.find_by_displayed_text("Система")

    @cached
    def navigation_information_sensor_tab(self):
        return self.qt_driver_wrapper.find_by_displayed_text("Датчик навигационой информации")

    @cached
    def ship_settings_tab(self):
        return self.qt_driver_wrapper.find_by_displayed_text("Настройки корабля")

    @cached
    def alarm_settings_tab(self):
        return self.qt_driver_wrapper.find_by_displayed_text("Настройка сигнализации")

    @cached
    def data_logging_panel_tab(self):
        return self.qt_driver_wrapper.find_by_displayed_text("Регистрация данных")

    @property
    def all_controls(self):
        yield self.system_panel_tab()
        yield self.navigation_information_sensor_tab()
        yield self.ship_settings_tab()
        yield self.alarm_settings_tab()
        yield self.generators_panel_tab()
        yield self.data_logging_panel_tab()


class NavigationPanel(EcdisControls):
    def __init__(self, qt_driver_wrapper):
        super().__init__(qt_driver_wrapper)

    @cached
    def man_over_board_button(self):
        return self.qt_driver_wrapper.find_by_external_id("manOverboardButton")

    @cached
    def ship_move_type_button(self):
        # return self.qt_driver_wrapper.find_by_external_id("shipMoveTypeButton")
        return self._get_next_button_down(button=self.man_over_board_button())

    @cached
    def arpa_button(self):
        return self._get_next_button_down(button=self.ship_move_type_button())

    @cached
    def radars_button(self):
        return self._get_next_button_down(button=self.arpa_button())

    @cached
    def ais_button(self):
        return self._get_next_button_down(button=self.radars_button())

    @cached
    def map_measurements_button(self):
        return self._get_next_button_down(button=self.ais_button())

    @cached
    def coordinates_amend_button(self):
        return self.qt_driver_wrapper.find_by_external_id("coordsAmendButton")

    @cached
    def marker_set_button(self):
        return self._get_next_button_down(button=self.coordinates_amend_button())

    @cached
    def from_another_source_button(self):
        return self._get_next_button_down(button=self.marker_set_button())

    @cached
    def mail_button(self):
        return self._get_next_button_down(button=self.from_another_source_button())

    @cached
    def split_screen_button(self):
        return self.qt_driver_wrapper.find_by_external_id("splitScreenButton")

    @cached
    def switch_slide_bar_button(self):
        return self.qt_driver_wrapper.find_by_external_id("switchSlideBarButton")

    @cached
    def switch_bottom_panel_button(self):
        return self.qt_driver_wrapper.find_by_external_id("switchBottomPanelButton")

    @cached
    def hide_al_button(self):
        return self.qt_driver_wrapper.find_by_external_id("hideAlButton")

    def _get_next_button_down(self, button):
        size = button.size
        x = button.location["x"]
        y = button.location["y"]

        controls = filter_by_size(controls=self.qt_driver_wrapper.qt_controls, size=size)
        controls = filter_by_x_location(controls=controls, x=x)
        controls = filter_by_y_location_greater(controls=controls, y=y)
        controls = sort_by_y_location(controls=controls)
        return controls[0]

    def _get_next_button_up(self, button):
        size = button.size
        x = button.location["x"]
        y = button.location["y"]

        controls = filter_by_size(controls=self.qt_driver_wrapper.qt_controls, size=size)
        controls = filter_by_x_location(controls=controls, x=x)
        controls = filter_by_y_location_less(controls=controls, y=y)
        controls = sort_by_y_location(controls=controls)
        return controls[-3]


if __name__ == "__main__":
    qt = qt_webdriver_wrapper.QtWebDriverWrapper('127.0.0.1', 9517)



    for button in buttons:
        print(button.size, button.location)
