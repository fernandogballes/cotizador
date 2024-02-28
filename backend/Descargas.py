from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import time
import os
from pathlib import Path
import shutil
from selenium.webdriver.common.action_chains import ActionChains


def descarga_ATR():
    url = 'https://www.mites.gob.es/es/estadisticas/condiciones_trabajo_relac_laborales/EAT/welcome.htm#'
    options = Options()
    #options.add_argument("-headless") 
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)  # Utilizar ChromeDriverManager para obtener la versión correcta
    driver.get(url)

    wait = WebDriverWait(driver, 20)  # Aumentar el tiempo de espera

    scrolled = 0
    max_scroll = 10
    scroll_increment = 350
    while scrolled < max_scroll:
        try:
            xpath = '/html/body/div[2]/div[2]/div/section/article/div/div[2]/div[1]/div[2]/div[3]/div/p/a'
            download_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Resultados detallados")))
            if download_button:
                download_button.click()
                break
        except TimeoutException as e:
            print("Tiempo de espera agotado:", e)
        except ElementClickInterceptedException as e:
            print("Error al hacer clic en el elemento:", e)
        except Exception as e:
            print("Error inesperado:", e)
        finally:
            driver.quit()

def descarga_ATR_1():
    url = 'https://www.mites.gob.es/es/estadisticas/condiciones_trabajo_relac_laborales/EAT/welcome.htm#'
    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    wait = WebDriverWait(driver, 20)

    try:
        # Desplazarse hacia abajo en la página
        driver.execute_script("window.scrollBy(0, 350);")

        # Esperar a que aparezca el botón que quieres pulsar
        download_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Resultados detallados")))
        
        # Hacer clic en el botón
        download_button.click()
    except Exception as e:
        print("Error:", e)
    finally:
        # Cerrar el navegador al finalizar la acción
        driver.quit()

if __name__ == '__main__':
    descarga_ATR_1()


