import pandas as pd
import os
from pathlib import Path
from tqdm import tqdm


# Configs
DATA_PATH = Path("../../01_dados/dados_ons")
OUT_PATH = Path("../../01_dados/dados_ons_merged")


def merge_data():
    """
    Função que mescla todos os arquivos CSV em cada pasta do caminho dos dados e salva 
    em uma nova pasta no caminho de saída.
    """

    # Itera sobre cada pasta no caminho dos dados
    for folder in os.listdir(DATA_PATH):
        print(f"Merging CSV files in folder: {folder}")
        # Define o caminho da pasta atual
        folder_path = DATA_PATH / folder

        # Lista para armazenar todos os DataFrames
        data_frames = []

        # Itera sobre cada arquivo na pasta atual
        for file_name in tqdm(os.listdir(folder_path)):
            # Define o caminho do arquivo atual
            file_path = folder_path / file_name

            # Tenta ler o arquivo CSV em um DataFrame
            try:
                df = pd.read_csv(file_path, encoding="iso-8859-1", on_bad_lines='skip')
                # Adiciona o DataFrame à lista
                data_frames.append(df)
            except pd.errors.EmptyDataError:  # Ignora arquivos CSV vazios
                pass
        
        try:
                    
            # Concatena todos os DataFrames em um único DataFrame ao longo do eixo das colunas
            merged_df = pd.concat(data_frames)

            # Define o caminho da pasta de saída e cria a pasta se ela não existir
            out_folder = OUT_PATH / folder
            out_folder.mkdir(parents=True, exist_ok=True)

            # Define o caminho do arquivo de saída e salva o DataFrame mesclado como um arquivo CSV
            out_file_path = out_folder / f"{folder}.csv"
            merged_df.to_csv(out_file_path, index=False)
            
        except:
            pass    

    print("Finished merging all CSV files.")


if __name__ == "__main__":
    merge_data()