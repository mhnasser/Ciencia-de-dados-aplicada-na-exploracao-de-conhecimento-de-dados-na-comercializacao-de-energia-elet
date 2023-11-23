import os
import time
import pandas as pd
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from tqdm import tqdm
from utils_tools import get_aneel_page, extract_aneel_table_data
import warnings

warnings.filterwarnings("ignore")

DOWNLOAD_PATH = Path("C:/Users/moham/Downloads")
OUTPUT_PATH = Path("../../01_dados/dados_aneel")
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

def get_aneel_data():
    browser = get_aneel_page()
    
    tipo_geracao = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.NAME, "IdTipoGeracao"))
    )       

    df_list = list()

    for tipo in range(1,9):
        
        tipo_geracao = Select(browser.find_element(By.NAME, "IdTipoGeracao"))  
        tipo_geracao.options[tipo].click()
        browser.find_element(By.NAME, "buscar").click()
        time.sleep(10)
        df_list.append(extract_aneel_table_data(browser))
        
        while True:
            try:
                # Check if the "Next" button exists
                next_button = browser.find_element(By.LINK_TEXT, "Próximo")
            except NoSuchElementException:
                # If the "Next" button is not found, break out of the loop
                break

            # Click the "Next" button to go to the next page
            next_button.click()
            time.sleep(10)
            df_list.append(extract_aneel_table_data(browser))
            
    df_final = pd.concat(df_list)
    df_final.to_csv(OUTPUT_PATH / 'dados.aneel.csv', index=False, encoding='utf-8')
    
if __name__ == "__main__":
    
    get_aneel_data()