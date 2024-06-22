# Pymol analysis of semi-homogeneous cliques

(Part of my master thesis)

All proteins in cliques are aligned to the last element of a clique. They are also colored by their taxonomy: 
- red - Viruses
- blue - Bacteria
- gold - Archaea
- green - Eukaryota

## Instalation

```
git clone git@github.com:ChrisGadek1/pymol-cliques-analysis.git
cd pymol-cliques-analysis
```

## Run
(remember to set up virtual environment first and be sure Pymol is installed and available directly from command "pymol")
```
pip3 install -r requirements.txt
python3 run.py --clique_number=[0..n] --clique_json_path=[some path]
```

Loaded clique and cliques group can be adjusted by changing named arguments: `cliques_number` and `cliques_json_path`.

In example, loading a clique with id 1 (second, because the cliques are indexed from 0) from Archaea-Bacteria-Eukaryota group can be loaded with this command:

```
python3 run.py --clique_number=1 --clique_json_path="./archaea_bacteria_viruses_cliques.json"
```
