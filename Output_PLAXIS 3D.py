"""
Извлечение данных и запись в EXCEL
"""
import tkinter.filedialog as dialog
from tkinter import Tk
import openpyxl as xls
import plxscripting.easy as plx
import confg


def filter_point_coord(x, y, uz):
    coords_without_repeat = []
    for key in range(len(x)):
        if [x[key], y[key]] not in coords_without_repeat:
            coords_without_repeat.append([x[key], y[key], uz[key]])
    return coords_without_repeat


def path(string):
    """
    На вход подается путь к файлу. Функция обрезает путь до типа файла с точкой.
    """
    return str(string.split('.p3d')[0])  # .split(str) возвращает массив из частей строк, которые разрезаются по аргументу


def main():
    # Подключение к Plaxis Input, Plaxis Output
    s_i, g_i = plx.new_server(f'{confg.pl_ip}', confg.pl_port, password=f'{confg.pl_password}')
    s_o, g_o = plx.new_server(f'{confg.pl_ip}', confg.pl_port_out, password=f'{confg.pl_password}')


    # Открытие окна выбора файлов
    Tk().withdraw()
    files = dialog.askopenfilenames(title="Выберите файлы для импорта", filetypes=[
        ("Plaxis3D", "*.p3d *.plx"), ("All Files", "*")])

    print(f'всего файлов: {len(files)}')

    for file in files:
        s_i.open(filename=file)
        # g_i.Phases[-1] это последняя стадия расчета
        if g_i.Phases[-1].LogInfo != '0':  # проверяем последнюю фазу на завершение расчета по ней, если не завершен
                                           # то создаем файл txt и переходим к следующему файлу расчета
            with open(path(file)+'.txt', 'w', encoding='UTF-8') as text:   # функция path(string) описана выше
                """
                Обычная конструкция открытия файла на запись. Если файла нет - он будет создан, если есть - все записи в
                этом файле будут стерты и записаны новые.
                """
                print('No solve!!!', file=text)
            continue

        s_o.open(filename=file)
        beam_X = []
        beam_Y = []
        beam_Uz = []
        for beam in g_o.Beams:
            # g_o.Phases[-1] это последняя стадия расчета
            beam_X += g_o.getresults(beam, g_o.Phases[-1], g_o.ResultTypes.Beam.X, 'node', True)[:]
            beam_Y += g_o.getresults(beam, g_o.Phases[-1], g_o.ResultTypes.Beam.Y, 'node', True)[:]
            beam_Uz += g_o.getresults(beam, g_o.Phases[-1], g_o.ResultTypes.Beam.Uz, 'node', True)[:]

        coords_beams = filter_point_coord(beam_X, beam_Y, beam_Uz)  # склеиваем 3 массива в один
        coords_beams.sort(key=lambda point: (point[1], point[0]))  # сортируем совместно координаты по Y и X. По Y приоретет, затем по X при одном значении Y. -point[] -- сортировка будет по убыванию.

        # Запись в файл ОК
        wb = xls.Workbook()
        sheet = wb.active
        sheet.title = 'Осадки балки'

        sheet.append(['X, m', 'Y, m', 'Uz, m'])

        for coord in coords_beams:
            sheet.append([coord[0], coord[1], coord[2]])

        wb.save(f'{path(file)}.xlsx')  # функция path(string) описана выше
        print(f'ВСЕ ОК: {file}')


if __name__ == "__main__":
    main()
