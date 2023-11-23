import os
import time
from pathlib import Path
from selenium.webdriver.common.by import By
from tqdm import tqdm
from utils_tools import get_ons_dataset_links
import warnings

warnings.filterwarnings("ignore")

DOWNLOAD_PATH = Path("C:/Users/moham/Downloads")
OUTPUT_PATH = Path("../../01_dados/dados_ons")
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)


def download_files():
    """ 
    Função que baixa arquivos de dados do site da ONS.
    """
    
    # Chama a função get_ons_dataset_links() para obter os links e o objeto do navegador
    links, browser = get_ons_dataset_links()
    
    print("Iniciando Download dos Arquivos")

    # Itera sobre cada link na lista de links
    for link in links:
        # Navega para a página da web do link atual
        browser.get(link)

        # Encontra todos os botões de download na página da web
        download_buttons = browser.find_elements(By.CSS_SELECTOR, ".resource-url-analytics")

        # Obtém o nome da pasta a partir do link (o nome base do URL)
        folder_name = os.path.basename(link)
        print(f"\n{folder_name}")

        # Se o nome da pasta não é 'bacia_contorno', cria uma nova pasta com esse nome
        if folder_name != "bacia_contorno":
            folder_path = OUTPUT_PATH / folder_name
            folder_path.mkdir(exist_ok=True)

            # Itera sobre cada botão de download e baixa o arquivo correspondente
            for button in tqdm(download_buttons, desc="File Download Progress", unit="file"):
                url = button.get_attribute("href")

                # Se o URL termina com '.csv', baixa o arquivo
                if url.endswith(".csv"):
                    filename = os.path.basename(url)
                    try:
                        # Define o caminho onde o arquivo baixado será armazenado temporariamente
                        downloaded_file = DOWNLOAD_PATH / filename

                        # Navega para o URL para iniciar o download
                        browser.get(url)

                        # Aguarda até que o arquivo seja baixado
                        while not os.path.exists(downloaded_file):
                            time.sleep(1)

                        # Limpa a saída do console
                        os.system('cls')
                        
                        # Move o arquivo baixado para a pasta correta
                        downloaded_file.rename(folder_path / filename)
                        os.remove(DOWNLOAD_PATH / downloaded_file)
                        
                    except Exception as e:
                        os.remove(DOWNLOAD_PATH / downloaded_file)
                        # Em caso de qualquer exceção, imprime a exceção e continua com o próximo arquivo
                        print(f"Error: {e}")
                        
                        # Limpa a saída do console
                        os.system('cls')
                        pass


if __name__ == "__main__":
    download_files()