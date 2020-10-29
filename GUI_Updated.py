# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 21:44:21 2020

@author: USER
"""

import PySimpleGUI as sg
import numpy as np
from pickle import load

# ADD TITLE COLOUR ,title_color='white'
sg.theme('DefaultNoMoreNagging')	# Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Developed by Hoang D. Nguyen')],
            [sg.Text('Ulsan National Institute of Science and Technology (UNIST)')],
            [sg.Text('Ulsan, South Korea')],
            [sg.Text('Email: nguyenhoangkt712@unist.ac.kr')],
            #[sg.Text('Input parameters')],
            [sg.Frame(layout=[
            [sg.Text('PGA',size=(10, 1)),sg.InputText(key='-f1-'),sg.Text('g')],
            [sg.Text('PGV',size=(10, 1)), sg.InputText(key='-f2-'),sg.Text('m/s')],
            [sg.Text('PGD',size=(10, 1)), sg.InputText(key='-f3-'),sg.Text('m')],
            [sg.Text('fDo',size=(10, 1)), sg.InputText(key='-f4-'),sg.Text('Hz')],
            [sg.Text('Mw',size=(10, 1)), sg.InputText(key='-f5-'),sg.Text('Mw')],
            [sg.Text('Rjb',size=(10, 1)), sg.InputText(key='-f6-'),sg.Text('km')],
            [sg.Text('Soil type',size=(10, 1)), sg.InputText(key='-f7-'),sg.Text('1-A,2-B,3-C,4-D')],
            [sg.Text('Sa(T1,5%)',size=(10, 1)), sg.InputText(key='-f8-'),sg.Text('g')],
            [sg.Text('Sa(T2,5%)',size=(10, 1)), sg.InputText(key='-f9-'),sg.Text('g')],
            [sg.Text('Sa(T3,5%)',size=(10, 1)), sg.InputText(key='-f10-'),sg.Text('g')],
            [sg.Text('Ns',size=(10, 1)), sg.InputText(key='-f11-'),sg.Text('1,2,...')],
            [sg.Text('Nb',size=(10, 1)),sg.InputText(key='-f12-'),sg.Text('1,2,...')]],title='Input parameters')],
            [sg.Frame(layout=[
            [sg.Text('Mamimum Top Drift',size=(22, 1)),sg.InputText(key='-O1-',size=(30, 1)),sg.Text('%')],       
            [sg.Text('Mamimum Interstory Drift',size=(22, 1)), sg.InputText(key='-O2-',size=(30, 1)),sg.Text('%')]],title='Output')],
            [sg.Button('Predict'), sg.Button('Default'),sg.Button('Cancel')] ]

# Create the Window
window = sg.Window('Predict The Global Response of Plane Steel Moment Resisting Frames', layout)

#load model

# model of all groups
filename = 'BestModel_Total_TotalDrift.sav'
loaded_model_disp = load(open(filename, 'rb'))
filename = 'BestModel_Total_Drift.sav'
loaded_model_drift = load(open(filename, 'rb'))

# model case 6
filename1 = 'BestModel_Case6_TotalDrift.sav'
loaded_model_disp_Case6 = load(open(filename1, 'rb'))
filename1 = 'BestModel_Case6_Drift.sav'
loaded_model_drift_Case6 = load(open(filename1, 'rb'))


# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':	# if user closes window or clicks cancel
        break
    if event == 'Default':
        window['-f1-'].update('Must be filled')
        window['-f2-'].update('Must be filled')
        window['-f3-'].update('Must be filled')
        window['-f4-'].update('Must be filled')
        window['-f8-'].update('Must be filled')
        window['-f9-'].update('Must be filled')
        window['-f10-'].update('Must be filled')
        window['-f11-'].update('Must be filled')
        window['-f12-'].update('Must be filled')
    if event == 'Predict':

        if values['-f1-'] == '' or values['-f2-'] == '' or values['-f3-'] == '' or values['-f4-'] == ''  or values['-f8-'] == '' or values['-f9-'] == '' or values['-f10-'] == ''or values['-f11-'] == ''or values['-f12-'] == '':
            window['-O1-'].update('Please fill the input variables')
            window['-O2-'].update('Please fill the input variables')

        elif values['-f1-'] == 'Must be filled' or values['-f2-'] == 'Must be filled' or values['-f3-'] == 'Must be filled' or values['-f4-'] == 'Must be filled'  or values['-f8-'] == 'Must be filled' or values['-f9-'] == 'Must be filled' or values['-f10-'] == 'Must be filled'or values['-f11-'] == 'Must be filled'or values['-f12-'] == 'Must be filled':
            window['-O1-'].update('Please fill the input variables')
            window['-O2-'].update('Please fill the input variables')
            
    
        elif (values['-f5-'] == '' or values['-f6-'] == '' or values['-f7-'] == ''):  
            x_test=np.array([[values['-f1-'],values['-f2-'], values['-f3-'],values['-f4-'],values['-f8-'],values['-f9-'],values['-f10-'],values['-f11-'],values['-f12-']]])
            y_pred_disp = loaded_model_disp_Case6.predict(x_test)
            y_pred_drift = loaded_model_drift_Case6.predict(x_test)


            #print('You entered ',y_pred_disp[0]*100,y_pred_drift[0]*100)
            window['-O1-'].update(np.round((y_pred_disp[0]*100),4))
            window['-O2-'].update(np.round((y_pred_drift[0]*100),4))
            
        
        else:    
            x_test=np.array([[values['-f1-'],values['-f2-'], values['-f3-'],values['-f4-'],values['-f5-'],values['-f6-'],values['-f7-'],values['-f8-'],values['-f9-'],values['-f10-'],values['-f11-'],values['-f12-']]])
            print(x_test)
            y_pred_disp = loaded_model_disp.predict(x_test)
            y_pred_drift= loaded_model_drift.predict(x_test)
            print('You entered ',y_pred_disp[0]*100,y_pred_drift[0]*100)
            window['-O1-'].update(np.round((y_pred_disp[0]*100),4))
            window['-O2-'].update(np.round((y_pred_drift[0]*100),4))

    
window.close()
