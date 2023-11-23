import os
import sqlite3
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import warnings

warnings.filterwarnings("ignore")

def create_database():
    # Define the parent directory where the subfolders and CSV files are located
    parent_directory = Path("../../01_dados/dados_ons_merged")

    # Define the path to the folder where you want to store the database file
    database_folder = Path("../../01_dados/database")

    # Define the name of the SQLite3 database file, including the path to the database folder
    database_file = database_folder / "database.db"

    if not os.path.isfile(database_file):
        # Create the database file if it doesn't already exist
        conn = sqlite3.connect(database_file)
        conn.close()

    # Connect to the database file and create a cursor object
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    for folder_name in tqdm(os.listdir(parent_directory), desc="Updating Database: "):
        if os.path.isdir(os.path.join(parent_directory, folder_name)):
            # Define the path to the CSV file in the current folder
            csv_file = os.path.join(parent_directory, folder_name, f"{folder_name}.csv")

            if os.path.isfile(csv_file):
                # Read the CSV file into a pandas DataFrame
                df = pd.read_csv(csv_file)

                # Define the name of the table as the folder name with hyphens replaced by underscores
                table_name = folder_name.replace("-", "_")

                # Save the DataFrame to the database as a new table
                df.to_sql(table_name, conn, if_exists="replace", index=False)

    # Commit changes to the database and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":

    create_database()