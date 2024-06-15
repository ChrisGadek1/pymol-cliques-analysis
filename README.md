# Pymol analysis of semi-homogeneous cliques

(Part of master thesis)

## Instalation

```
git clone git@github.com:ChrisGadek1/pymol-cliques-analysis.git
cd pymol-cliques-analysis
```

## Run

```
pip3 install -r requirements.txt
python3 run.py --clique_number=[0..n] --clique_json_path=[some path]
```

Loaded clique and cliques group can be adjusted by changing named arguments: `cliques_number` and `cliques_json_path`.

In example, loading 5-th clique from Archaea-Bacteria-Eukaryota group can be loaded with this command:

```
python3 run.py --clique_number=5 --clique_json_path="./archaea_bacteria_viruses_cliques.json"
```