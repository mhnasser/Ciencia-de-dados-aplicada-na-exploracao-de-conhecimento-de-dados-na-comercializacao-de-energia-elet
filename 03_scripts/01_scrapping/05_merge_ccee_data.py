import pandas as pd
import os
from pathlib import Path
from tqdm import tqdm


# Configs
DATA_PATH = Path("../../01_dados/dados_ccee")
OUT_PATH = Path("../../01_dados/dados_ccee_merged")


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
                df = pd.read_csv(file_path, encoding="utf-8", on_bad_lines='skip')
                # Adiciona o DataFrame à lista
                data_frames.append(df)
                
            except pd.errors.EmptyDataError:  # Ignora arquivos CSV vazios
                pass
                    
        # Concatena todos os DataFrames em um único DataFrame ao longo do eixo das colunas
        merged_df = pd.concat(data_frames, axis=0, ignore_index=True)
        
        # Ajusta as colunas de dia e hora para timestamp
        if 'Hora' in merged_df.columns:
    
            merged_df['Dia'] = pd.to_datetime(merged_df['Dia'], errors='coerce')
            merged_df['day'] = merged_df['Dia'].dt.day
            
            merged_df['din_instante'] = merged_df['Dia'].dt.strftime('%Y-%m') + \
                            merged_df['day'].apply(lambda x: f'-{str(x).zfill(2)}') + \
                            merged_df['Hora'].apply(lambda x:f' {str(int((x-1)%24))}:00:00' if len(str(int((x-1)%24))) > 1 else f' 0{str(int((x-1)%24))}:00:00')
            
            merged_df = merged_df.drop(['Dia', 'Hora','day'], axis=1)

        # Define o caminho da pasta de saída e cria a pasta se ela não existir
        out_folder = OUT_PATH / folder
        out_folder.mkdir(parents=True, exist_ok=True)

        # Define o caminho do arquivo de saída e salva o DataFrame mesclado como um arquivo CSV
        out_file_path = out_folder / f"{folder}.csv"
        merged_df.to_csv(out_file_path, index=False, encoding="utf-8")


    print("Finished merging all CSV files.")


if __name__ == "__main__":
    merge_data()