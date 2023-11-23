import os
import zipfile
import warnings
import pandas as pd
from pathlib import Path
from selenium.webdriver.common.by import By
from tqdm import tqdm
from utils_tools import get_ccee_dataset_links
from time import sleep

warnings.filterwarnings("ignore")

DOWNLOAD_PATH = Path("C:/Users/moham/Downloads")
OUTPUT_PATH = Path("../../01_dados/dados_ccee")
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

index = {
    2: 'dados_horarios',
    3: 'usinas_com_cvu',
    4: 'biomassa',
    5: 'eolicas',
    6: 'hidraulicas_nao_mre',
    7: 'hidraulicas_mre',
    8: 'demais_usinas'
}

def download_files():
    # Obtem os links e a instância do navegador com a função get_ccee_dataset_links()
    links, browser = get_ccee_dataset_links()

    print("\nIniciando Download dos Arquivos")
    # Limpa a saída do console
    os.system('cls')

    # Para cada link na lista de links
    for link in links:
        try:
            # Navega até o link para iniciar o download do arquivo
            browser.get(link)

            # Espera até o download ser completo
            while True:
                # Obtém a lista de arquivos no diretório de download
                files = os.listdir(DOWNLOAD_PATH)
                # Filtra a lista para incluir apenas arquivos .zip que contêm 'InfoHorário_' no nome
                zip_files = [file for file in files if file.endswith('.zip') and 'InfoHorário_' in file]
                # Se algum arquivo .zip foi encontrado, interrompe o loop de espera
                if zip_files:
                    break
                sleep(3)

            # Obtém o primeiro arquivo .zip da lista de arquivos .zip
            downloaded_file = zip_files[0]

            # Extrai o sufixo do nome do arquivo baixado
            sufix = downloaded_file.split('_')[1].split('.')[0]
            print('\n[+]', sufix)

            # Extrai o arquivo .zip
            with zipfile.ZipFile(DOWNLOAD_PATH / downloaded_file, 'r') as zip_ref:
                zip_ref.extractall(DOWNLOAD_PATH)

            # Remove o arquivo .zip após a extração
            os.remove(DOWNLOAD_PATH / downloaded_file)

            # Para cada folha na lista de chaves do dicionário index
            for sheet in tqdm(index.keys(), desc="Excel Data Extracting..."):
                # Cria um nome de arquivo temporário usando a folha e o sufixo
                temp_file = index[sheet] + sufix + '.csv'
                # Define o caminho da pasta e cria a pasta se ela não existir
                folder_path = OUTPUT_PATH / index[sheet]
                folder_path.mkdir(parents=True, exist_ok=True)

                # Obtém a lista de arquivos Excel no diretório de download
                excel_files = [f for f in os.listdir(DOWNLOAD_PATH) if '01.InfoHorário_' in f and 'xlsx' in f]
                # Obtém o primeiro arquivo Excel da lista
                excel_file = excel_files[0]

                # Lê a folha especificada do arquivo Excel em um DataFrame
                df_temp = pd.read_excel(DOWNLOAD_PATH / excel_file,
                                        sheet_name=sheet,
                                        header=14,
                                        engine='openpyxl')

                # Remove a coluna 'Unnamed: 0' e linhas com NaN na coluna 'Dia'
                df_temp.drop('Unnamed: 0', axis=1, inplace=True)
                df_temp.dropna(subset='Dia', inplace=True)

                # Salva o DataFrame em um arquivo .csv no caminho especificado
                df_temp.to_csv(folder_path / temp_file, index=False)
                print(folder_path / temp_file)

            # Remove o arquivo Excel após o processamento
            os.remove(DOWNLOAD_PATH / excel_file)

            # Limpa a saída do console
            os.system('cls')

        except Exception as e:
            print(f"Error: {e}")
            pass

    print('\nDownload Dados CCEE Concluído!!')

if __name__ == "__main__":
    download_files()