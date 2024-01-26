from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pdfminer.high_level import extract_text, extract_pages
from pdfminer.layout import LTTextContainer
import pyautogui
import os
import random
import re 


def iniciar_driver():
    chrome_options = Options()

    arguments = ['--lang=pt-BR', '--window-size=1375,760']

    for argument in arguments:
        chrome_options.add_argument(argument)

    chrome_options.add_experimental_option('prefs', {
        'download.default_directory': 'C:\\Users\\Cliente C&C\\Desktop\\Teste_Automação\\Downloads',
        'download.directory_upgrade': True,
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1

    })

    driver = webdriver.Chrome(options=chrome_options)
    
    wait = WebDriverWait(
        driver,
        10,
        poll_frequency=1,
        ignored_exceptions=[
            NoSuchElementException,
            ElementNotVisibleException,
            ElementNotSelectableException,
        ]
    )
    return driver, wait 

driver, wait = iniciar_driver()

def download_pdf():
    # 1 Acessar o site
    driver.get('http://diariooficial.imprensaoficial.com.br/nav_v6/index.asp?c=34031&e=20231030&p=1')
    sleep(10)

    # Mudar Iframe
    iframe = driver.find_element(By.XPATH, "//iframe[@id='topFrame']")
    driver.switch_to.frame(iframe)

    # Em Nome da Seção selecionar abaixo de Negócios Públicos a opção Educação
    nome_secao_dropdown = driver.find_element(By.XPATH, "//select[@id='pg']") 
    opcoes = Select(nome_secao_dropdown)

    opcoes.select_by_visible_text('____Educação .... 137')
    sleep(10)

    # Download PDF
    botao_download = pyautogui.locateCenterOnScreen('botao.png')
    sleep(5)
    pyautogui.moveTo(botao_download[0],botao_download[1],duration=2)
    sleep(2)
    pyautogui.click()
    sleep(2)
    pyautogui.hotkey('enter')
    sleep(2)


def lidando_com_pdf():
    padrao = r'TOMADA DE PREÇOS Nº: (\d{2}/\d{5}/\d{2}/\d{2})'
        
    for page_layout in extract_pages('pg_0137.pdf'):
        for element in page_layout:
            if isinstance(element,LTTextContainer):
                if padrao in element.get_text:
                    print(element.get_text())

    # Salvar texto do PDF para um arquivo de texto 
    with open('tomada_de_precos.txt', 'w') as file:
        file.write(element)