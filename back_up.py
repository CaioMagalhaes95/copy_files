import os
import shutil
from datetime import datetime
import logging
import time


# criar log para visualização
LOG_FILE = "back_up.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def get_files_from_network(network_folder):
    # Obtém a lista de arquivos da pasta copartilhada (network_folder)
    files = []
    for file_name in os.listdir(network_folder):
        file_path = os.path.join(network_folder, file_name)

        if os.path.isfile(file_path):
            modified_time = datetime.utcfromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%dT%H:%M:%S')
            files.append({'name': file_name, 'modified': modified_time})
        return files

def sync_files(network_folder, local_dir):
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
    try:

        for item in os.listdir(network_folder):
            network_item_path = os.path.join(network_folder, item)
            local_item_path = os.path.join(local_dir, item)
            

        # network_files = get_files_from_network(network_folder)

            if os.path.isdir(network_item_path):
                sync_files(network_item_path, local_item_path)

        # for network_file in network_files:
        #     local_item_path = os.path.join(local_dir, network_file['name'])
        #     network_file_path = os.path.join(network_folder, network_file['name'])

            else:
                if os.path.exists(local_item_path):
                    # local_modified_time = datetime.utcfromtimestamp(os.path.getmtime(local_item_path)).strftime('%Y-%m-%dT%H:%M:%S')
                    local_modified_time = os.path.getmtime(local_item_path)
                    # network_modified_time = datetime.utcfromtimestamp(os.path.getmtime(network_item_path)).strftime('%Y-%m-%dT%H:%M:%S')
                    network_modified_time = os.path.getmtime(network_item_path)

                    if local_modified_time < network_modified_time:
                        logging.info(f"updating file {local_item_path}")
                        shutil.copy2(network_file_path, local_item_path)
                    else:
                        logging.info(f"File {local_item_path} is up to date")
                else:
                    logging.info(f"Downloading new file {local_item_path}...")
                    shutil.copy2(network_item_path, local_item_path)
    except Exception as e:
        logging.error(f"Error: {network_item_path}: {e}")

if __name__ == "__main__":
    network_folder = "C:\\Users\\JMARQ125\\OneDrive - azureforD\\LABOEM\\2 - Homologacoes - Anexo C1"
    local_directory = "C:\\Users\\JMARQ125\\BackUp - Homologacoes - Anexo C1"

    while True:
        logging.info(f"starting sync at {datetime.now().strftime('%Y - %m - %d %H:%M:%S')}")
        try:
            sync_files(network_folder, local_directory)
        except Exception as e:
            logging.info(f"Error during sync: {e}")

        logging.info("Sync completo. Aguardando proxima checagem")
        time.sleep(1800)
