# -*- coding: utf-8 -*-
import allure
import cv
import pyautogui
import pytest

from allure_commons.types import AttachmentType
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

import time

DATA_ROUTE = [(110, 341),
              (231, 249),
              (473, 459),
              (443, 525),
              (198, 528),
              (154, 370)]

CLICK_COORDINATES = [(457, 761), (556, 761),
                     (457, 791), (556, 791),
                     (457, 821), (556, 821),
                     (457, 851), (556, 851),
                     (457, 881), (556, 881),
                     (457, 911), (556, 911)]

save_x, save_y = cv.get_save_button() or (1059, 572)
cancel_x, cancel_y = cv.get_cancel_button() or (1064, 580)
delete_icon_x, delete_icon_y = cv.get_delete_icon() or (1141, 710)
upload_icon_coordinate_x, upload_icon_coordinate_y = cv.get_upload_icon() or (1542, 768)
offset_helper = cv.OffsetHelper(1920, 1080)


@allure.feature("ECDIS route_planing")
@allure.story("ECDIS route_planning: test_check_geo_coord_visibility")
def test_check_geo_coord_visibility(ecdis_ui):
    with allure.step("Проверка отображения верхней панели координат"):
        ecdis_ui.qt_driver_wrapper.qt_driver.save_screenshot("screenshot_before_reg.png")
        allure.attach(ecdis_ui.qt_driver_wrapper.qt_driver.get_screenshot_as_png(),
                  name="geo1", attachment_type=AttachmentType.PNG)
        assert cv.check_geo_coord_module("screenshot_before_reg.png")


@allure.feature("ECDIS route_planing")
@allure.story("ECDIS route_planning: add_new_route")
@pytest.mark.parametrize("route_name", ["testroute"])
def test_add_new_route(ecdis_ui, route_name):
    with allure.step("Открываем вкладку предварительной прокладки маршрутов"):
        ecdis_ui.window_plugin_panels.route_planing_panel_tab().click()

    with allure.step("Жмем на кнопку \"Добавить новый маршрут\""):
        add_button = ecdis_ui.route_planning_panel.add_new_route_button()
        add_button.click()

    with allure.step("Добавляем имя маршрута"):
        ac = ActionChains(ecdis_ui.qt_driver_wrapper.qt_driver)
        ac.send_keys(route_name).perform()
        ac.reset_actions()

        # Make screen to find "Apply button"

        ecdis_ui.qt_driver_wrapper.qt_driver.save_screenshot("screenshot_before_reg.png")
        allure.attach(ecdis_ui.qt_driver_wrapper.qt_driver.get_screenshot_as_png(),
                      name="scr1", attachment_type=AttachmentType.PNG)

    with allure.step("Жмем кнопку подтвердить"):
        x, y = cv.get_text_coordinates_by_image_color("screenshot_before_reg.png", text="Подтвердить")
        assert x, y
        pyautogui.click(x, y)

    with allure.step("Проверяем, что маршрут был создан"):
        ecdis_ui.qt_driver_wrapper.qt_driver.save_screenshot("screenshot_after_reg.png")
        allure.attach(ecdis_ui.qt_driver_wrapper.qt_driver.get_screenshot_as_png(),
                      name="scr2", attachment_type=AttachmentType.PNG)
        assert cv.get_text_coordinates_by_image_color("screenshot_after_reg.png", lang="eng", text=route_name)


@allure.feature("ECDIS route_planing")
@allure.story("ECDIS route_planning: several_route_points:map")
def test_check_complicated_route_points_map(ecdis_ui):

    for i in range(len(DATA_ROUTE)):
        with allure.step(f"Переводим курсор на карту и ставим {i + 1} точку"):
            pyautogui.moveTo(*DATA_ROUTE[i])
            pyautogui.click(*DATA_ROUTE[i])
            ecdis_ui.qt_driver_wrapper.qt_driver.save_screenshot(f"route_point_{i + 1}.png")
            allure.attach(ecdis_ui.qt_driver_wrapper.qt_driver.get_screenshot_as_png(),
                          name=f"route_{i + 1}", attachment_type=AttachmentType.PNG)
            assert cv.check_coord_complience(f"route_point_{i + 1}.png")


@allure.feature("ECDIS route_planing")
@allure.story("ECDIS route_planning: several_route_points_table")
def test_check_several_route_points_table(ecdis_ui):
    # Delete previous route_points
    for _ in range(6):
        ecdis_ui.route_planning_panel.delete_route_point_button().click()

    # Same route_points adding through table
    with allure.step("проверяем, что из скриншота таблицы получены все координаты"):
        text_to_fill = cv.get_coord_from_table("route_point_6.png", base=True)

        assert len(text_to_fill) == 12

    with allure.step("заполняем таблицу полученными координатами путевых точек и делаем скриншот"):
        for index, text in enumerate(text_to_fill):
            if not index % 2:
                ecdis_ui.route_planning_panel.add_route_point_button().click()

            pyautogui.click(*CLICK_COORDINATES[index])
            pyautogui.press("home")
            pyautogui.write(text)
            pyautogui.press("enter")

    ecdis_ui.qt_driver_wrapper.qt_driver.save_screenshot("screen_comp_final.png")

    allure.attach(ecdis_ui.qt_driver_wrapper.qt_driver.get_screenshot_as_png(),
                  name="table_1", attachment_type=AttachmentType.PNG)

    assert cv.equal("screen_comp_final.png", "route_point_6.png")


@allure.feature("ECDIS route_planing")
@allure.story("ECDIS route_planning: several_route_points:map")
@pytest.mark.parametrize("route_points_number", [4])
def test_check_several_route_points_map(ecdis_ui, route_points_number):
    # Delete previous route_points
    for _ in range(6):
        ecdis_ui.route_planning_panel.delete_route_point_button().click()

    # TODO: parametrize
    x, y = 240, 460
    route_distance = 172

    for i in range(route_points_number):
        with allure.step(f"Переводим курсор на карту и ставим путевую точку {i + 1} под углом 90 градусов"):
            pyautogui.moveTo(x + i * route_distance, y)
            pyautogui.click(x + i * route_distance, y)
            time.sleep(1)
            allure.attach(ecdis_ui.qt_driver_wrapper.qt_driver.get_screenshot_as_png(),
                          name=f"route_{i}", attachment_type=AttachmentType.PNG)

    # TODO: parametrize
    pyautogui.scroll(1, 400, 466)
    pyautogui.scroll(1, 400, 466)

    with allure.step("проверяем, что при приближении участка карты "
                     "корректно отображаеются атрибуты (скорость, угол, расстояние) участков маршрута"):

        ecdis_ui.qt_driver_wrapper.qt_driver.save_screenshot(f"route_point_zoom_check.png")
        allure.attach(ecdis_ui.qt_driver_wrapper.qt_driver.get_screenshot_as_png(),
                      name="route_segment_attrs", attachment_type=AttachmentType.PNG)
        assert cv.check_route_details_by_image_color("route_point_zoom_check.png")

    # TODO: parametrize
    pyautogui.scroll(-1, 400, 466)
    pyautogui.scroll(-1, 400, 466)


@allure.feature("ECDIS route_planing")
@allure.story("ECDIS route_planning: add_control_points")
def test_add_control_points(ecdis_ui):
    with allure.step("жмем на вкладку \"Контрольные точки\" и сохраняем скриншот"):
        ecdis_ui.route_planning_panel.control_points_tab().click()
        ecdis_ui.qt_driver_wrapper.qt_driver.save_screenshot("save_add_control_before.png")
        allure.attach(ecdis_ui.qt_driver_wrapper.qt_driver.get_screenshot_as_png(),
                      name="add_control_point_1", attachment_type=AttachmentType.PNG)

    # TODO: parametrize
    x, y = (279, 460)
    control_point_distance = 172
    number_of_control_points = 3

    for i in range(number_of_control_points):
        with allure.step(f"Переводим курсор на карту и ставим {i + 1} контольную точку"):
            pyautogui.moveTo(x + i * control_point_distance, y)
            pyautogui.click(x + i * control_point_distance, y)
            ecdis_ui.qt_driver_wrapper.qt_driver.save_screenshot(f"control_point_{i}.png")
            allure.attach(ecdis_ui.qt_driver_wrapper.qt_driver.get_screenshot_as_png(),
                          name=f"control_{i}", attachment_type=AttachmentType.PNG)

    with allure.step("Проверяем, что количество строк в таблице контрольных точек соответствует кол-во"
                     "заведенных контрольных точек"):
        assert cv.get_row_number_of_table("control_point_2.png") == number_of_control_points



@allure.feature("ECDIS route_planing")
@allure.story("ECDIS route_planning: save_route")
def test_save_route(ecdis_ui):
    with allure.step("Жмем на кнопку \"Сохранить маршрут\" "):
        ecdis_ui.route_planning_panel.save_route_button().click()

    with allure.step("В диалоговом окне выбираем \"Да\""):
        ecdis_ui.qt_driver_wrapper.qt_driver.save_screenshot("save_accept.png")
        allure.attach(ecdis_ui.qt_driver_wrapper.qt_driver.get_screenshot_as_png(),
                      name="save_1", attachment_type=AttachmentType.PNG)
        pyautogui.click(save_x, save_y)

    with allure.step("Проверяем, что маршрут был корректно сохранен"):
        ecdis_ui.qt_driver_wrapper.qt_driver.save_screenshot("save_final.png")
        allure.attach(ecdis_ui.qt_driver_wrapper.qt_driver.get_screenshot_as_png(),
                      name="save_2", attachment_type=AttachmentType.PNG)
        assert cv.get_text_coordinates_by_image_thresh("save_final.png", lang="eng", text="testroute")


@allure.feature("ECDIS route_planing")
@allure.story("ECDIS route_planning: delete_two_route_point")
def test_delete_two_route_points(ecdis_ui):
    coord_list_before = cv.get_coord_from_table("drag_and_drop_after.png")

    with allure.step("Удаляем 2 и 3 точку маршрута"):
        allure.attach(ecdis_ui.qt_driver_wrapper.qt_driver.get_screenshot_as_png(),
                      name="delete_1", attachment_type=AttachmentType.PNG)

        # Delete third route point
        pyautogui.click(*CLICK_COORDINATES[2])
        ecdis_ui.route_planning_panel.delete_route_point_button().click()

        # Delete second route point
        pyautogui.click(*CLICK_COORDINATES[4])
        ecdis_ui.route_planning_panel.delete_route_point_button().click()

        ecdis_ui.qt_driver_wrapper.qt_driver.save_screenshot("route_points_deleted.png")
        coord_list_after = cv.get_coord_from_table("route_points_deleted.png")

    with allure.step("Проверяем, что удаление прошло корректно"):
        allure.attach(ecdis_ui.qt_driver_wrapper.qt_driver.get_screenshot_as_png(),
                      name="delete_2", attachment_type=AttachmentType.PNG)

        assert len(coord_list_before) != len(coord_list_after)


@allure.feature("ECDIS route_planing")
@allure.story("ECDIS route_planning: cancel_edit_points")
def test_check_cancel_edit(ecdis_ui):
    with allure.step("Проверяем, что текущие координаты отличаются от сохраненных"):
        coord_list_before = cv.get_coord_from_table("save_final.png")
        ecdis_ui.qt_driver_wrapper.qt_driver.save_screenshot("route_points_deleted_current.png")
        coord_list_current = cv.get_coord_from_table("route_points_deleted_current.png")
        assert coord_list_before != coord_list_current

    with allure.step("Нажимаем кнопку отменить и проверяем совпадение координат с сохраненными"):
        ecdis_ui.route_planning_panel.cancel_changes_button().click()
        ecdis_ui.qt_driver_wrapper.qt_driver.save_screenshot("route_points_deleted_after_cancel.png")

        pyautogui.click(cancel_x, cancel_y)
        time.sleep(1)

        ecdis_ui.qt_driver_wrapper.qt_driver.save_screenshot("route_points_deleted_final.png")
        coord_list_final = cv.get_coord_from_table("route_points_deleted_final.png")
        allure.attach(ecdis_ui.qt_driver_wrapper.qt_driver.get_screenshot_as_png(),
                      name="cancel_1", attachment_type=AttachmentType.PNG)
        assert all(elem in coord_list_final for elem in coord_list_before)


@allure.feature("ECDIS route_planing")
@allure.story("ECDIS route_planning: attach_big_txt_file_to_control_point")
def test_attach_big_txt_file_to_control_point(ecdis_ui):
    file_name = "Big.txt"
    with allure.step("жмем кнопку \"загрузить файл\""):
        pyautogui.moveTo(upload_icon_coordinate_x, upload_icon_coordinate_y)
        pyautogui.click(upload_icon_coordinate_x, upload_icon_coordinate_y)

        # Choose folder
        pyautogui.write("test_resources")
        pyautogui.press("enter")

        # Choose file to upload
        pyautogui.write(file_name)
        pyautogui.press("enter")

        pyautogui.moveTo((upload_icon_coordinate_x + 44, upload_icon_coordinate_y))
        ecdis_ui.qt_driver_wrapper.qt_driver.save_screenshot("BigTxt.png")

        allure.attach(ecdis_ui.qt_driver_wrapper.qt_driver.get_screenshot_as_png(),
                      name="file_1", attachment_type=AttachmentType.PNG)

    with allure.step(f"Проверяем, что файл {file_name} загрузился"):
        assert cv.check_file_uploaded("BigTxt.png", file_name=file_name)

    with allure.step("Удаляем файл"):
        # Delete attachment
        pyautogui.click(upload_icon_coordinate_x + 44, upload_icon_coordinate_y, button="right")
        pyautogui.click((upload_icon_coordinate_x + 46, upload_icon_coordinate_y + 44))
        time.sleep(1)


@allure.feature("ECDIS route_planing")
@allure.story("ECDIS route_planning: attach_big_bmp_file_to_control_point")
def test_attach_big_bmp_file_to_control_point(ecdis_ui):
    file_name = "BigBmp.bmp"
    with allure.step("Жмем кнопку \"загрузить файл\""):
        pyautogui.moveTo(upload_icon_coordinate_x, upload_icon_coordinate_y)
        pyautogui.click(upload_icon_coordinate_x, upload_icon_coordinate_y)
        time.sleep(1)

        pyautogui.write(file_name)
        pyautogui.press("enter")

        pyautogui.moveTo((upload_icon_coordinate_x + 22, upload_icon_coordinate_y))
        ecdis_ui.qt_driver_wrapper.qt_driver.save_screenshot("BigBmp.png")

        allure.attach(ecdis_ui.qt_driver_wrapper.qt_driver.get_screenshot_as_png(),
                      name="file_2", attachment_type=AttachmentType.PNG)

    with allure.step(f"Проверяем, что файл {file_name} загрузился"):
        assert cv.check_file_uploaded("BigBmp.png", file_name=file_name)

    with allure.step("Удаляем файл"):
        # Delete attachment
        pyautogui.click(upload_icon_coordinate_x + 22, upload_icon_coordinate_y, button="right")
        pyautogui.click(upload_icon_coordinate_x + 24, upload_icon_coordinate_y + 22)
        time.sleep(1)


@allure.feature("ECDIS route_planing")
@allure.story("ECDIS route_planning: attach_big_jpg_file_to_control_point")
def test_attach_big_jpg_file_to_control_point(ecdis_ui):
    file_name = "BigJpg.jpg"
    with allure.step("Жмем кнопку \"загрузить файл\""):
        pyautogui.moveTo(upload_icon_coordinate_x, upload_icon_coordinate_y)
        pyautogui.click(upload_icon_coordinate_x, upload_icon_coordinate_y)
        time.sleep(1)

        pyautogui.write(file_name)
        pyautogui.press("enter")

        pyautogui.moveTo((upload_icon_coordinate_x + 22, upload_icon_coordinate_y))
        ecdis_ui.qt_driver_wrapper.qt_driver.save_screenshot("BigJpg.png")

        allure.attach(ecdis_ui.qt_driver_wrapper.qt_driver.get_screenshot_as_png(),
                      name="file_3", attachment_type=AttachmentType.PNG)

    with allure.step(f"Проверяем, что файл {file_name} загрузился"):
        assert cv.check_file_uploaded("BigJpg.png", file_name=file_name)

    # Delete attachment
    with allure.step("Удаляем файл"):
        pyautogui.click(upload_icon_coordinate_x + 22, upload_icon_coordinate_y, button="right")
        pyautogui.click(upload_icon_coordinate_x + 24, upload_icon_coordinate_y + 22)
        time.sleep(1)


@allure.feature("ECDIS route_planing")
@allure.story("ECDIS route_planning: attach_big_png_file_to_control_point")
def test_attach_big_png_file_to_control_point(ecdis_ui):
    file_name = "BigPng.png"
    with allure.step("Жмем кнопку \"загрузить файл\""):
        pyautogui.moveTo(upload_icon_coordinate_x, upload_icon_coordinate_y)
        pyautogui.click(upload_icon_coordinate_x, upload_icon_coordinate_y)
        time.sleep(1)

        pyautogui.write(file_name)
        pyautogui.press("enter")

        pyautogui.moveTo((upload_icon_coordinate_x + 22, upload_icon_coordinate_y))
        ecdis_ui.qt_driver_wrapper.qt_driver.save_screenshot("BigPng.png")

        allure.attach(ecdis_ui.qt_driver_wrapper.qt_driver.get_screenshot_as_png(),
                      name="file_4", attachment_type=AttachmentType.PNG)

    with allure.step(f"Проверяем, что файл {file_name} загрузился"):
        assert cv.check_file_uploaded("BigPng.png", file_name=file_name)

    # Delete attachment
    with allure.step("Удаляем файл"):
        pyautogui.click(upload_icon_coordinate_x + 22, upload_icon_coordinate_y, button="right")
        pyautogui.click(upload_icon_coordinate_x + 24, upload_icon_coordinate_y + 22)
        time.sleep(1)


@allure.feature("ECDIS route_planing")
@allure.story("ECDIS route_planning: attach_empty_text_file_to_control_point")
def test_attach_empty_text_file_to_control_point(ecdis_ui):
    file_name = "EmptyText.txt"
    with allure.step("Жмем кнопку \"загрузить файл\""):
        pyautogui.moveTo(upload_icon_coordinate_x, upload_icon_coordinate_y)
        pyautogui.click(upload_icon_coordinate_x, upload_icon_coordinate_y)
        time.sleep(1)

        pyautogui.write(file_name)
        pyautogui.press("enter")

        pyautogui.moveTo((upload_icon_coordinate_x + 44, upload_icon_coordinate_y))
        ecdis_ui.qt_driver_wrapper.qt_driver.save_screenshot("EmptyText.png")

        allure.attach(ecdis_ui.qt_driver_wrapper.qt_driver.get_screenshot_as_png(),
                      name="file_5", attachment_type=AttachmentType.PNG)

    with allure.step(f"Проверяем, что файл {file_name} загрузился"):
        assert cv.check_file_uploaded("EmptyText.png", file_name=file_name)

    with allure.step("Удаляем файл"):
        pyautogui.click(upload_icon_coordinate_x + 44, upload_icon_coordinate_y, button="right")
        pyautogui.click((upload_icon_coordinate_x + 46, upload_icon_coordinate_y + 44))
        time.sleep(1)


@allure.feature("ECDIS route_planing")
@allure.story("ECDIS route_planning: attach_no_jpeg_file_to_control_point")
def test_attach_no_jpeg_file_to_control_point(ecdis_ui):
    file_name = "NoJpeg.jpg"
    with allure.step("Жмем кнопку \"загрузить файл\""):
        pyautogui.moveTo(upload_icon_coordinate_x, upload_icon_coordinate_y)
        pyautogui.click(upload_icon_coordinate_x, upload_icon_coordinate_y)
        time.sleep(1)

        pyautogui.write(file_name)
        pyautogui.press("enter")

        pyautogui.moveTo((upload_icon_coordinate_x + 22, upload_icon_coordinate_y))
        ecdis_ui.qt_driver_wrapper.qt_driver.save_screenshot("NoJpeg.png")

        allure.attach(ecdis_ui.qt_driver_wrapper.qt_driver.get_screenshot_as_png(),
                      name="file_6", attachment_type=AttachmentType.PNG)

    with allure.step(f"Проверяем, что файл {file_name} загрузился"):
        assert cv.check_file_uploaded("NoJpeg.png", file_name=file_name)

    with allure.step("Удаляем файл"):
        pyautogui.click(upload_icon_coordinate_x + 22, upload_icon_coordinate_y, button="right")
        pyautogui.click(upload_icon_coordinate_x + 24, upload_icon_coordinate_y + 22)
        time.sleep(1)


@allure.feature("ECDIS route_planing")
@allure.story("ECDIS route_planning: attach_no_png_file_to_control_point")
def test_attach_no_png_file_to_control(ecdis_ui):
    file_name = "NoPng.png"
    with allure.step("Жмем кнопку \"загрузить файл\""):
        pyautogui.moveTo(upload_icon_coordinate_x, upload_icon_coordinate_y)
        pyautogui.click(upload_icon_coordinate_x, upload_icon_coordinate_y)
        time.sleep(1)

        pyautogui.write(file_name)
        pyautogui.press("enter")

        pyautogui.moveTo((upload_icon_coordinate_x + 22, upload_icon_coordinate_y))
        ecdis_ui.qt_driver_wrapper.qt_driver.save_screenshot("NoPng.png")

        allure.attach(ecdis_ui.qt_driver_wrapper.qt_driver.get_screenshot_as_png(),
                      name="file_7", attachment_type=AttachmentType.PNG)

    with allure.step(f"Проверяем, что файл {file_name} загрузился"):
        assert cv.check_file_uploaded("NoPng.png", file_name=file_name)

    with allure.step("Удаляем файл"):
        pyautogui.click(upload_icon_coordinate_x + 22, upload_icon_coordinate_y, button="right")
        pyautogui.click(upload_icon_coordinate_x + 24, upload_icon_coordinate_y + 22)
        time.sleep(1)


@allure.feature("ECDIS route_planing")
@allure.story("ECDIS route_planning: attach_not_so_big_text_file_to_control_point")
def test_attach_not_so_big_text_file_to_control_point(ecdis_ui):
    file_name = "NotSoBig.txt"
    with allure.step("Жмем кнопку \"загрузить файл\""):
        pyautogui.moveTo(upload_icon_coordinate_x, upload_icon_coordinate_y)
        pyautogui.click(upload_icon_coordinate_x, upload_icon_coordinate_y)
        time.sleep(1)

        pyautogui.write(file_name)
        pyautogui.press("enter")

        pyautogui.moveTo((upload_icon_coordinate_x + 44, upload_icon_coordinate_y))
        ecdis_ui.qt_driver_wrapper.qt_driver.save_screenshot("NotSoBig.png")

        allure.attach(ecdis_ui.qt_driver_wrapper.qt_driver.get_screenshot_as_png(),
                      name="file_8", attachment_type=AttachmentType.PNG)

    with allure.step(f"Проверяем, что файл {file_name} загрузился"):
        assert cv.check_file_uploaded("NotSoBig.png", file_name=file_name)

    with allure.step("Удаляем файл"):
        pyautogui.click(upload_icon_coordinate_x + 44, upload_icon_coordinate_y, button="right")
        pyautogui.click(upload_icon_coordinate_x + 46, upload_icon_coordinate_y + 44)
        time.sleep(1)


@allure.feature("ECDIS route_planing")
@allure.story("ECDIS route_planning: attach_reg_text_file_to_control_point")
def test_attach_reg_text_file_to_control_point(ecdis_ui):
    file_name = "RegText.txt"
    with allure.step("Жмем кнопку \"Загрузить файл\""):
        pyautogui.moveTo(upload_icon_coordinate_x, upload_icon_coordinate_y)
        pyautogui.click(upload_icon_coordinate_x, upload_icon_coordinate_y)
        time.sleep(1)

        pyautogui.write(file_name)
        pyautogui.press("enter")

        pyautogui.moveTo((upload_icon_coordinate_x + 44, upload_icon_coordinate_y))
        ecdis_ui.qt_driver_wrapper.qt_driver.save_screenshot("RegText.png")

        allure.attach(ecdis_ui.qt_driver_wrapper.qt_driver.get_screenshot_as_png(),
                      name="file_9", attachment_type=AttachmentType.PNG)

    with allure.step(f"Проверяем, что файл {file_name} загрузился"):
        assert cv.check_file_uploaded("RegText.png", file_name=file_name)

    with allure.step("Удаляем файл"):
        pyautogui.click(upload_icon_coordinate_x + 44, upload_icon_coordinate_y, button="right")
        pyautogui.click(upload_icon_coordinate_x + 46, upload_icon_coordinate_y + 44)
        time.sleep(1)


@allure.feature("ECDIS route_planing")
@allure.story("ECDIS route_planning: attach_very_very_big_file_to_control_point")
def test_attach_very_big_text_file_to_control_point(ecdis_ui):
    file_name = "VeryVeryBig.txt"
    with allure.step("Жмем кнопку \"Загрузить файл\""):
        pyautogui.moveTo(upload_icon_coordinate_x, upload_icon_coordinate_y)
        pyautogui.click(upload_icon_coordinate_x, upload_icon_coordinate_y)
        time.sleep(1)

        pyautogui.write(file_name)
        pyautogui.press("enter")

        pyautogui.moveTo(upload_icon_coordinate_x + 44, upload_icon_coordinate_y)
        ecdis_ui.qt_driver_wrapper.qt_driver.save_screenshot("VeryVeryBig.png")

        allure.attach(ecdis_ui.qt_driver_wrapper.qt_driver.get_screenshot_as_png(),
                      name="file_10", attachment_type=AttachmentType.PNG)

    with allure.step(f"Проверяем, что файл {file_name} загрузился"):
        assert cv.check_file_uploaded("VeryVeryBig.png", file_name=file_name)

    with allure.step("Удаляем файл"):
        pyautogui.click(upload_icon_coordinate_x + 44, upload_icon_coordinate_y, button="right")
        pyautogui.click((upload_icon_coordinate_x + 46, upload_icon_coordinate_y + 44))
        time.sleep(1)


@allure.feature("ECDIS route_planing")
@allure.story("ECDIS route_planning: attach_reg_bmp_file_to_control_point")
def test_attach_reg_bmp_file_to_control(ecdis_ui):
    file_name = "RegBmp.bmp"
    with allure.step("Жмем кнопку \"Загрузить файл\""):
        pyautogui.moveTo(upload_icon_coordinate_x, upload_icon_coordinate_y)
        pyautogui.click(upload_icon_coordinate_x, upload_icon_coordinate_y)
        time.sleep(1)

        pyautogui.write(file_name)
        pyautogui.press("enter")

        pyautogui.moveTo((upload_icon_coordinate_x + 22, upload_icon_coordinate_y))
        ecdis_ui.qt_driver_wrapper.qt_driver.save_screenshot("RegBmp.png")

        allure.attach(ecdis_ui.qt_driver_wrapper.qt_driver.get_screenshot_as_png(),
                      name="file_11", attachment_type=AttachmentType.PNG)

    with allure.step(f"Проверяем, что файл {file_name} загрузился"):
        assert cv.check_file_uploaded("RegBmp.png", file_name=file_name)

    with allure.step("Удаляем файл"):
        pyautogui.click(upload_icon_coordinate_x + 22, upload_icon_coordinate_y, button="right")
        pyautogui.click(upload_icon_coordinate_x + 24, upload_icon_coordinate_y + 22)
        time.sleep(1)


@allure.feature("ECDIS route_planing")
@allure.story("ECDIS route_planning: attach_reg_jpg_file_to_control_point")
def test_attach_reg_jpg_file_to_control(ecdis_ui):
    file_name = "RegJpg.jpg"
    with allure.step("Жмем кнопку \"Загрузить файл\""):
        pyautogui.moveTo(upload_icon_coordinate_x, upload_icon_coordinate_y)
        pyautogui.click(upload_icon_coordinate_x, upload_icon_coordinate_y)
        time.sleep(1)

        pyautogui.write(file_name)
        pyautogui.press("enter")

        pyautogui.moveTo((upload_icon_coordinate_x + 22, upload_icon_coordinate_y))
        ecdis_ui.qt_driver_wrapper.qt_driver.save_screenshot("RegJpg.png")

        allure.attach(ecdis_ui.qt_driver_wrapper.qt_driver.get_screenshot_as_png(),
                      name="file_12", attachment_type=AttachmentType.PNG)

    with allure.step(f"Проверяем, что файл {file_name} загрузился"):
        assert cv.check_file_uploaded("RegJpg.png", file_name=file_name)

    with allure.step("Удаляем файл"):
        pyautogui.click(upload_icon_coordinate_x + 22, upload_icon_coordinate_y, button="right")
        pyautogui.click(upload_icon_coordinate_x + 24, upload_icon_coordinate_y + 22)
        time.sleep(1)


@allure.feature("ECDIS route_planing")
@allure.story("ECDIS route_planning: attach_reg_png_file_to_control_point")
def test_attach_reg_png_file_to_control(ecdis_ui):
    file_name = "RegPng.png"
    with allure.step("Жмем кнопку \"Загрузить файл\""):
        pyautogui.moveTo(upload_icon_coordinate_x, upload_icon_coordinate_y)
        pyautogui.click(upload_icon_coordinate_x, upload_icon_coordinate_y)
        time.sleep(1)

        pyautogui.write("RegPng.png")
        pyautogui.press("enter")

        pyautogui.moveTo((upload_icon_coordinate_x + 22, upload_icon_coordinate_y))
        ecdis_ui.qt_driver_wrapper.qt_driver.save_screenshot("RegPng.png")

        allure.attach(ecdis_ui.qt_driver_wrapper.qt_driver.get_screenshot_as_png(),
                      name="file_13", attachment_type=AttachmentType.PNG)

    with allure.step(f"Проверяем, что файл {file_name} загрузился"):
        assert cv.check_file_uploaded("RegPng.png", file_name=file_name)

    with allure.step("Удаляем файл"):
        pyautogui.click(upload_icon_coordinate_x + 22, upload_icon_coordinate_y, button="right")
        pyautogui.click(upload_icon_coordinate_x + 24, upload_icon_coordinate_y + 22)
        time.sleep(1)


@allure.feature("ECDIS route_planing")
@allure.story("ECDIS route_planning: attach_reg_png_file_to_control_point")
def test_attach_no_resolution_file_to_control_point(ecdis_ui):
    file_name = "NoResolution"
    with allure.step("Жмем кнопку \"Загрузить файл\""):
        pyautogui.moveTo(upload_icon_coordinate_x, upload_icon_coordinate_y)
        pyautogui.click(upload_icon_coordinate_x, upload_icon_coordinate_y)
        time.sleep(1)

        pyautogui.write(file_name)
        pyautogui.press("enter")

        ecdis_ui.qt_driver_wrapper.qt_driver.save_screenshot("NoResolution.png")
        time.sleep(1)

        pyautogui.press("enter")
        pyautogui.press("esc")


def test_delete_control_points(ecdis_ui):
    with allure.step("жмем на кнопку \"Удалить контрольную точку\""):
        pyautogui.click(delete_icon_x, delete_icon_y)
        ecdis_ui.qt_driver_wrapper.qt_driver.save_screenshot("delete_control.png")
        allure.attach(ecdis_ui.qt_driver_wrapper.qt_driver.get_screenshot_as_png(),
                      name="delete_control_1", attachment_type=AttachmentType.PNG)

    with allure.step("Проверяем, что удаление прошло успешно"):
        assert cv.get_row_number_of_table("delete_control.png") == 2


@allure.feature("ECDIS route_planing")
@allure.story("ECDIS route_planning: delete_route")
def test_delete_route(ecdis_ui):
    with allure.step("Выбираем сохраненный маршрут"):
        saved_route_coord = cv.get_text_coordinates_by_image_thresh("save_final.png", lang="eng", text="testroute")
        assert saved_route_coord
        pyautogui.click(*saved_route_coord)

    with allure.step("Удаляем сохраненный маршрут"):
        ecdis_ui.route_planning_panel.delete_route_button().click()
        ecdis_ui.qt_driver_wrapper.qt_driver.save_screenshot("delete_route_accept.png")
        x, y = cv.get_text_coordinates_by_image_color("delete_route_accept.png", lang="rus", text="Подтвердить")
        assert x, y
        pyautogui.click(x, y)

    with allure.step("Проверяем, что маршрут удален"):
        ecdis_ui.qt_driver_wrapper.qt_driver.save_screenshot("deleted_route.png")
        allure.attach(ecdis_ui.qt_driver_wrapper.qt_driver.get_screenshot_as_png(),
                      name="delete_route", attachment_type=AttachmentType.PNG)
        assert not cv.get_text_coordinates_by_image_thresh("deleted_route.png", lang="eng", text="testroute")


