import os
import time
from pathlib import Path
from selenium.webdriver.common.by import By
from tqdm import tqdm
from utils_tools import *
import warnings

warnings.filterwarnings("ignore")


# Configs
DOWNLOAD_PATH = Path("C:/Users/moham/Downloads")
OUTPUT_PATH = Path("../../01_dados/dados_ons")
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)


def update_files():
    """ 
    Função para atualizar os arquivos de dados do site da ONS.
    """
    
    # Obtém os links e o objeto do navegador da função get_ons_dataset_links()
    links, browser = get_ons_dataset_links()
    print("Iniciando Atualizações dos Arquivos")
    
    # Limpa a saída do console
    clear_console_output()

    # Itera sobre cada link na lista de links
    for link in tqdm(links, unit="file", desc="Atualização dos Arquivos:"):
        # Navega para a página da web do link atual
        browser.get(link)

        # Encontra todos os botões de download na página da web
        download_buttons = browser.find_elements(By.CSS_SELECTOR, ".resource-url-analytics")

        # Obtém o nome da pasta a partir do link (o nome base do URL)
        folder_name = os.path.basename(link)

        # Se o nome da pasta é 'bacia_contorno', continua com o próximo link
        if folder_name == "bacia_contorno":
            continue

        # Define o caminho da pasta
        folder_path = OUTPUT_PATH / folder_name

        # Se há 4 ou menos botões de download, baixa os arquivos sem filtrar por ano
        # Caso contrário, baixa apenas os arquivos do ano "2023"
        if len(download_buttons) <= 4:
            download_files(browser,download_buttons, folder_path)
        else:
            download_files(browser, download_buttons, folder_path, "2023")

        # Limpa a saída do console
        clear_console_output()

def download_files(browser, download_buttons, folder_path, year=None):
    """
    Função para baixar arquivos da página da web.
    
    Args:
        browser: Elemento web criado pela função get_ons_dataset_links
        download_buttons: Lista de elementos que contêm os botões de download.
        folder_path: Caminho da pasta onde os arquivos serão salvos.
        year: Ano dos arquivos a serem baixados. Se None, baixa todos os arquivos pois nesses casos o arquivo é único.
    """
    
    # Itera sobre cada botão de download
    for button in download_buttons:
        url = button.get_attribute("href")
        
        # Se o URL termina com '.csv' e (não há filtro de ano ou o ano está no URL), baixa o arquivo
        if url.endswith(".csv") and (year is None or year in url):
            filename = os.path.basename(url)
            downloaded_file = DOWNLOAD_PATH / filename

            # Inicia o download do arquivo
            browser.get(url)

            # Aguarda até que o arquivo seja baixado
            while not os.path.exists(downloaded_file):
                time.sleep(1)

            # Se o arquivo já existe no local de destino, remove o arquivo existente
            if os.path.exists(folder_path / filename):
                os.remove(folder_path / filename)

            # Move o arquivo baixado para o local de destino
            downloaded_file.rename(folder_path / filename)

def clear_console_output():
    """ 
    Função para limpar a saída do console.
    """
    os.system("cls" if os.name == "nt" else "clear")  # Limpa a saída do console


if __name__ == "__main__":
    update_files()
    print("\nAtualização Concluida!!")