import warnings

import requests
import json
import os
import subprocess
import argparse
from tqdm import tqdm
import base64

parser=argparse.ArgumentParser()

parser.add_argument("--clique_number", help="Number of cliques proteins, which will be loaded to a pymol")
parser.add_argument("--clique_json_path", help="Path to json file containing ids of uniprot proteins involved in cliques")


args=parser.parse_args()
clique_json_path = args.clique_json_path if args.clique_json_path is not None else "./bacteria_eukaryota_viruses_cliques.json"


def encode_path(path):
    return base64.b64encode(path.encode("ascii")).decode("ascii")


def load_json_file():
    with open(clique_json_path, "r") as open_file:
        return json.load(open_file)


def get_protein(uniprot_accession):
    api_endpoint = "https://alphafold.ebi.ac.uk/api/prediction/"
    url = f"{api_endpoint}{uniprot_accession}"  # Construct the URL for API
    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        result = response.json()
        return result
    else:
        response.raise_for_status()


cliques_uniprot_ids = load_json_file()
cliques = list(cliques_uniprot_ids.values())[0]

def prepare_script(clique_number):
    set_grid = "set grid_mode,1"
    cliques_files_directory_path = os.path.abspath("./pdb_files/"+encode_path(clique_json_path)+"/clique_"+clique_number)
    load_files = ["load "+os.path.join(cliques_files_directory_path, file) for file in os.listdir(cliques_files_directory_path)]
    align_proteins = [f'align {cliques[int(clique_number)][i]}, {cliques[int(clique_number)][-1]}' for i in range(len(cliques[int(clique_number)]) - 1)]
    with open("cliques_loading.pml", "w") as new_script:
        new_script.write('\n'.join([set_grid] + load_files + align_proteins))


stats = {'failed': 0, 'succeed': 0}
print("Fetching PDB files")
for index, clique in enumerate(tqdm(list(cliques_uniprot_ids.values())[0])):
    clique_directory_path = "./pdb_files/"+encode_path(clique_json_path)+"/clique_"+str(index)
    if not os.path.exists(clique_directory_path):
        os.makedirs(clique_directory_path)
        for clique_element in clique:
            try:
                protein_info = get_protein(clique_element)
                pdb_url = protein_info[0].get('pdbUrl')
                pdb_data = requests.get(pdb_url).text
                with open(clique_directory_path+"/"+clique_element+".pdb", "w") as new_pdb_file:
                    new_pdb_file.write(pdb_data)
                stats['succeed'] += 1
            except:
                stats['failed'] += 1
    else:
        warnings.warn("directory "+clique_directory_path+" is not empty. Fetching stopped.")

clique_number = args.clique_number if args.clique_number is not None else 0
prepare_script(clique_number)

subprocess.run(["pymol", "cliques_loading.pml"])

