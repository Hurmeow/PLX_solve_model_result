"""
Разбивка сетки, расчет в Plaxis Input
"""
import tkinter.filedialog as dialog
from tkinter import Tk
import plxscripting.easy as plx
import confg

# Подключение к Plaxis Input
s_i, g_i = plx.new_server(f'{confg.pl_ip}', confg.pl_port, password=f'{confg.pl_password}')
# Открытие окна выбора файлов
Tk().withdraw()
files = dialog.askopenfilenames(title="Выберите файлы для импорта", filetypes=[
                                ("Plaxis3D", "*.p3d *.plx"), ("All Files", "*")])

print(f'всего файлов: {len(files)}')

for file in files:
    #print(file)
    s_i.open(filename=file)
    g_i.gotomesh()  # переход на вкладку mesh
    g_i.mesh(0.035, 256, True, 1.2, 0.005)  #_mesh 0.035 256 False
    g_i.gotostages()  # переход на вкладку расчета
    for phase in g_i.Phases[1:]:  # если с 0 то с фазой инициализации
        # Установка Solver type ()
        phase.Solver = 1  # Solver type: 0 - Picos, 1 - Pardiso и т.д.? равно команде _set Phase_N.Solver "Pardiso (multicore direct)"

    g_i.calculate(True)
    g_i.save()
