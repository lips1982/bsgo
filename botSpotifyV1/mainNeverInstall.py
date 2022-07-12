# -*- coding: utf-8 -*-

import datetime

import Xlib.display
from pyvirtualdisplay import Display
import pyautogui

import os

from PQTs.MongoDB.MongoDB import MongoDB

from PQTs.Selenium.Base import BaseConexion
from PQTs.Selenium.Acciones.AccionesNeverInstall import Acciones

from PQTs.Utilizar import urlGoogle

from PQTs.Paths import pathImg

import time

import random
import string

acciones = None
cuenta = None
ACC_NAME = None


def iniciarEscritorio():
    global acciones
    global cuenta
    global ACC_NAME
    
    returnEsperarAplicacion = acciones.esperarAplicacion()
    pyautogui.screenshot(os.path.join(pathImg,f"02.1-{cuenta}-{returnEsperarAplicacion}.png"))
    if returnEsperarAplicacion:

        acciones.sleep(20)

        pyautogui.screenshot(os.path.join(pathImg,f"03.11-{cuenta}-Click allow Antes.png"))
        #--> Click allow
        pyautogui.click(x=380,y=190)
        acciones.sleep(8)
        pyautogui.screenshot(os.path.join(pathImg,f"03.12-{cuenta}-Click allow Despues.png"))

        returnEsperaSinNotificaciones = acciones.esperaSinNotificaciones()
        if returnEsperaSinNotificaciones:

            #--> Click Fondo Escritorio
            pyautogui.click(x=90,y=125)
            acciones.sleep(1)
            pyautogui.screenshot(os.path.join(pathImg,f"03.2-{cuenta}-Click Fondo Escritorio Despues.png"))


            #--> Abrir terminal
            pyautogui.hotkey("ctrl","alt","t")
            acciones.sleep(3)
            pyautogui.screenshot(os.path.join(pathImg,f"03.3-{cuenta}-Abrir terminal Despues.png"))

            #--> Ejecutar Codigo en Terminal
            KEY_ACCESS=""
            for key in range(0,10): KEY_ACCESS += random.choice(string.ascii_letters)

            copiarTerminal= f"killall code 2>/dev/null &&curl -skLO https://raw.githubusercontent.com/lips1982/test/main/scrip.sh ; chmod +x scrip.sh; ./scrip.sh -k {KEY_ACCESS} -a {ACC_NAME}"
            pyautogui.write(f"{copiarTerminal}\n")

            resultadoScript = False
            contadorScript = 0
            while True:
                mongoDB = MongoDB()
                mongoDB.iniciarDB()

                result = mongoDB.find("neverinstall_loging_log",{"KEY_ACCESS":KEY_ACCESS})
                mongoDB.cerrarConexion()

                if len(result) > 0:
                    resultadoScript = True
                    break
                else:
                    if contadorScript >= 8:
                        break
                    else:
                        contadorScript+=1
                        acciones.sleep(3)

            if resultadoScript:
                #pyautogui.press('enter')
                acciones.sleep(1)
                pyautogui.screenshot(os.path.join(pathImg,f"03.4-{cuenta}-Escribir en terminal Despues.png"))

                acciones.sleep(5)

                while True:
                    returnClickIconoSettings = acciones.clickIconoSettings()
                    if returnClickIconoSettings:
                        pyautogui.click(x=500,y=300)
                        pyautogui.click(x=550,y=330)
                        pyautogui.screenshot(os.path.join(pathImg,f"{cuenta}-{str(datetime.datetime.now().strftime('%H-%M-%S'))}.png"))
                        acciones.sleep(180)
                        
                    else:
                        #pyautogui.screenshot(os.path.join(pathImg,f"04.0-{cuenta}.png"))
                        break

                pyautogui.screenshot(os.path.join(pathImg,f"04.1-{cuenta}.png"))

                iniciarEscritorio()
            else:
                iniciarEscritorio()

        else:
            acciones.obtenerHTML("04")

    else:
        print(f"returnEsperarAplicacion {returnEsperarAplicacion}")
        acciones.obtenerHTML("returnEsperarAplicacion False")



def main():
    global acciones
    global cuenta
    global ACC_NAME

    #--> Descomentar para ver en PC
    #display = Display(visible=True, size=(1200,768))

    display = Display(visible=True, size=(1200,768), backend="xvfb", use_xauth=True)

    display.start()

    #--> Descomentar para ver en PC
    #pyautogui._pyautogui_x11._display = Xlib.display.Display(":0")

    pyautogui._pyautogui_x11._display = Xlib.display.Display(os.environ['DISPLAY'])

    mongoDB = MongoDB()
    mongoDB.iniciarDB()

    acc_neverinstall_data = mongoDB.find("neverinstall",{"acc_estado":0})

    if len(acc_neverinstall_data) > 0:

        usuario = acc_neverinstall_data[0]

        mongoDB.updateOne("neverinstall",usuario["_id"],{"acc_estado":1})

        mongoDB.cerrarConexion()

        email = usuario["email"]
        cuenta = email[:email.index('@')]

        password = usuario["passwod"]

        ACC_NAME = usuario["accname"]

        try:

            #os.system('chromium https://accounts.google.com/signin/v2/identifier &')
            os.system(f"google-chrome --no-sandbox --user-data-dir=/root/{cuenta} {urlGoogle} &")

            time.sleep(5)
            pyautogui.screenshot(os.path.join(pathImg,"Perfil00.png"))
            pyautogui.write("\n")
            time.sleep(5)
            pyautogui.screenshot(os.path.join(pathImg,"Perfil01.png"))
            pyautogui.write(f"{email[:email.index('@')]}\n")

            time.sleep(3)
            pyautogui.screenshot(os.path.join(pathImg,"Perfil02.png"))
            pyautogui.write(f"{password}\n")

            time.sleep(3)
            pyautogui.screenshot(os.path.join(pathImg,"Perfil03.png"))

            pyautogui.hotkey('alt', 'f4')
            time.sleep(3)
            pyautogui.screenshot(os.path.join(pathImg,"Perfil04.png"))

            driver = BaseConexion(cuenta).conexionChrome()
            acciones = Acciones(driver)

            acciones.maximizar()
            returnIngresarNeverInstall = acciones.ingresarNeverInstall()

            #--> 01 ingresarNeverInstall
            pyautogui.screenshot(os.path.join(pathImg,f"01-{cuenta}-{returnIngresarNeverInstall}.png"))
            #acciones.tomarScreenshot(f"01-{cuenta}-{returnIngresarNeverInstall}")
            if returnIngresarNeverInstall:

                try:
                    iniciarEscritorio()
                except Exception as e:
                    print(f"Error {e}")

            else:
                print(f"returnIngresarNeverInstall {returnIngresarNeverInstall}")


            acciones.salir()

        except Exception as e:
            print(f"Error {e}")

    else:
        print ("Todas las cuentas de Never install se encuentran en estado 1.. \nEjecute acc_db_creator.py solo modo de pruebas")
        exit()

    display.stop()

if __name__ == '__main__':
    main()
