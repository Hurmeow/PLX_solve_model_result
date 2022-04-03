"""
Заготовки по Plaxis
"""
import tkinter.filedialog as dialog
import re
from tkinter import Tk

#import openpyxl as xls

#import plaxistools.telegram as telegram
import plxscripting.easy as plx
import confg

# Подключение к Plaxis Output
s_o, g_o = plx.new_server('{}'.format(confg.pl_ip), confg.pl_port_out, password='{}'.format(confg.pl_password))
s_i, g_i = plx.new_server('{}'.format(confg.pl_ip), confg.pl_port, password='{}'.format(confg.pl_password))
# Открытие окна выбора файлов
Tk().withdraw()
files = dialog.askopenfilenames(title="Выберите файлы для импорта", filetypes=[
                                ("Plaxis3D", "*.p3d *.plx"), ("All Files", "*")])

print('всего файлов: {}'.format(len(files)))


########################
def nameSoil_to_number_file(path):
    if re.search('_1_', path):
        return 'Песок1_средний_е052'
    elif re.search('_2_', path):
        return 'Песок2_средний_е062'
    elif re.search('_3_', path):
        return 'Песок3_мелкийе051'



def nameBeam_to_number_file(path):
    if re.search('_0.4.p3d', path):
        return 'СВГD04'
    elif re.search('_0.6.p3d', path):
        return 'СВГD06'
    elif re.search('_0.8.p3d', path):
        return 'СВГD08'


for file in files:
    print(file)
    s_i.open(filename=file)
    print(nameSoil_to_number_file(file))
    material = nameSoil_to_number_file(file)
    plate3D = nameBeam_to_number_file(file)
    for mat in g_i.Materials[:]:
        if mat.TypeName.value == 'SoilMat'and mat.Name.value == material: #'MaterialName': <Text {990762AF-8EAB-498E-9980-DF7A85B90414}>, 'MaterialNumber': <Integer {26F577F3-3428-4A15-91EF-E4B51CC16C4C}>,'Name': <Text {B509A6F3-0F3E-4680-9D80-20D5D435CA68}>
            print(mat.__dict__)
            material = mat
            print(f'Name: {mat.Name.value}, Material name: {mat.MaterialName.value}, Material Number: {mat.MaterialNumber.value}')
        elif mat.TypeName.value == 'PlateMat3D'and mat.Name.value == plate3D:
            plate3D = mat
            print(f'Name: {mat.Name.value}, Material name: {mat.MaterialName.value}, Material Number: {mat.MaterialNumber.value}')
        elif mat.TypeName.value == 'BeamMat':
            beam3D = mat
            print(f'Name: {mat.Name.value}, Material name: {mat.MaterialName.value}, Material Number: {mat.MaterialNumber.value}')


for file in files:
    #print(file)
    s_i.open(filename=file)
    #g_i.gotomesh()
    #g_i.mesh(0.035, 256, True, 1.2, 0.005)  #_mesh 0.035 256 False
    g_i.gotostages()  # переход на вкладку расчета
    for phase in g_i.Phases[1:2]:
        #print(phase.__dict__)
        print(g_i.Phases[2].Solver.__dict__.keys())
        print(g_i.Phases[2].Solver.__dict__['_property_name'])
        print(g_i.Phases[2].Solver.__dict__['_owner'].__dict__['_attr_cache'].keys())
        print(g_i.Phases[2].Solver.__dict__['_owner'].__dict__['_attr_cache']['LogInfo'].__dict__['_owner'].__dict__)
        print(g_i.Phases[2].Solver)
        g_i.Phases[2].Solver = 1
        print(g_i.Phases[2].Solver)
        #g_i.Phases[2].Solver = g_i.Phases[2].Solver.Pardiso
        #g_i.phase.Solver = 1
        #print(g_i.Phases[2].Solver.setproperties)
        #print(g_i.Phases[-1].Solver.commands.__dict__)
    #g_i.calculate(True)
    g_i.save()
