# -*- coding: utf-8 -*-

from PQTs.Selenium.Base import BaseAcciones

from PQTs.Utilizar import urlNeverInstall

from PQTs.Paths import pathImg

from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import os

from bs4 import BeautifulSoup



import pyautogui

class Acciones(BaseAcciones):

    def __init__(self, driver):
        self.driver = driver

      #----------------------#
     #---> Neverinstall <---#
    #----------------------#

    def ingresarNeverInstall(self):
        xpathBotonGoogle = (By.XPATH,'//button[@id="googleLogin"]')
        xpathElementoCarga = (By.XPATH,'//div[@class="load-inner"]')

        self.ir(urlNeverInstall)

        visibleBotonGoogle = self.explicitWaitElementoVisibility(11,xpathBotonGoogle)
        if visibleBotonGoogle:
            self.click(xpathBotonGoogle)
            self.explicitWaitElementoInvisibility(11,xpathElementoCarga)
            return True
        else:
            print(f"visibleBotonGoogle {visibleBotonGoogle}")
            return False

    def esperarAplicacion(self):
        xpathBotonResumeSpace = (By.XPATH, "//span[contains(text(),'Resume space')]")
        xpathBotonResumeApp = (By.XPATH, "//span[contains(text(),'Resume App')]")

        xpathDivFlexContainer = (By.XPATH, "//div[@id='flexContainer']")

        contador = 0
        while True:
            visibleDivFlexContainer = self.explicitWaitElementoVisibility(11,xpathDivFlexContainer)
            if visibleDivFlexContainer:

                scriptEsperarAplicacion = """
                const esperarAplicacion = () => {
                    return new Promise (resolve => {
                        let contadorNone = 0;
                        let intervaloExisteElemento = setInterval(() => {
                            let elementoDivFlexContainer = document.getElementById("flexContainer");
                            if (elementoDivFlexContainer) {
                                let elementoPadre = elementoDivFlexContainer.parentElement;
                                if (contadorNone >= 8) {
                                    clearInterval(intervaloExisteElemento);
                                    resolve(false);
                                } else if (elementoPadre.getAttribute("style").includes("none")) {
                                    contadorNone++;
                                } else {
                                    clearInterval(intervaloExisteElemento);
                                    resolve(true);
                                }
                            } else {
                                if (contadorNone >= 8) {
                                    clearInterval(intervaloExisteElemento);
                                    resolve(false);
                                } else contadorNone++;
                            }
                        }, 3000);
                    });
                }
                return await esperarAplicacion();
                """
                return self.executeScript(scriptEsperarAplicacion)
            
            else:
                visibleBotonResumeSpace = self.explicitWaitElementoVisibility(11,xpathBotonResumeSpace)
                if visibleBotonResumeSpace:
                    self.click(xpathBotonResumeSpace)
                else:
                    visibleBotonResumeApp = self.explicitWaitElementoVisibility(11,xpathBotonResumeApp)
                    if visibleBotonResumeApp:
                        self.click(xpathBotonResumeApp)
                    else:
                        if contador >= 8:
                            return False
                        else:
                            contador+=1


    def esperaSinNotificaciones(self):
        scriptEsperarSinNotificaciones = """
        const esperarSinNotificaciones = () => {
            return new Promise (resolve => {
                let contadorNotificaciones = 0;
                let intervaloExisteNotificaciones = setInterval(() => {
                    let elementosNotificaciones = document.querySelectorAll("div[data-testid='timed-notification']");
                    if (elementosNotificaciones.length === 0) {
                        clearInterval(intervaloExisteNotificaciones);
                        resolve(true);
                    } else {
                        if (contadorNotificaciones >= 8) {
                            clearInterval(intervaloExisteNotificaciones);
                            resolve(false);
                        } else contadorNotificaciones++;
                    }
                }, 3000);
            });
        }
        return await esperarSinNotificaciones();
        """
        return self.executeScript(scriptEsperarSinNotificaciones)

    def clickIconoSettings(self):
        scriptClickIconoSettings = """
        let elementoDivIconoSettings = document.getElementById("settings");
        if (elementoDivIconoSettings) {
            elementoDivIconoSettings.click();
            return true;
        } else return false;
        """
        self.executeScript(scriptClickIconoSettings)
        self.sleep(2)
        return self.executeScript(scriptClickIconoSettings)


      #----------------------#
     #---> Herramientas <---#
    #----------------------#

    def tomarScreenshot(self,nombreImagen):
        self.screenshot(nombreImagen)

    def obtenerHTML(self,nombre):
        html_source_code = self.executeScript("return document.body.innerHTML;")
        soup = BeautifulSoup(html_source_code, 'html.parser')
        with open(os.path.join(pathImg,f"{nombre}.html"), 'w') as f:
            f.write(str(soup))