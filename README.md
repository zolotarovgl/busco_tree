# BUSCO-based phylogeny   


## TODOs  
- add the scripts for a tree cleaning for GeneRax   


```bash
sbatch --time=06:00:00 submit.sh 
```

Example
```bash
BUSCODIR=/users/asebe/xgraubove/genomes/annotation_busco/ # path to Xavi's busco analysis directory
IQTREE=/users/xgraubove/Programes/iqtree-2.1.0-Linux/bin/iqtree2

python busco_tree.py --busco_dir $BUSCODIR --iqtree $IQTREE --species_list species_list --fmin 1 --ncpu 4
python plot.py results_busco/supermatrix.treefile
```
