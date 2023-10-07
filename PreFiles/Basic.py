# Main Program ICOS

#VENV
#Create
    #python -m venv ICOSenv
#Activate
    #ICOSenv\Scripts\activate
#upgrade
    #pip install --upgrade pip

#Import packages
import PySimpleGUI as sg

layout = [[sg.Text("Hello from Exmaple ICOS")], [sg.Button("OK")]]

# Create the window
window = sg.Window("Demo", layout)

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "OK" or event == sg.WIN_CLOSED:
        break

window.close()