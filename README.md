# BUSCO-based phylogeny   


## TODOs  
- add the scripts for a tree cleaning for GeneRax   


```bash
sbatch --time=06:00:00 submit.sh 
```

Example
```bash
python busco_tree.py --busco_dir $BUSCODIR --iqtree $IQTREE --species_list species_list --fmin 1 --ncpu 4
python plot.py results_busco/supermatrix.treefile
```
