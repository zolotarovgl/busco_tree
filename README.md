# BUSCO-based phylogeny   

Identify single BUSCO orthologs in `species_list` and build a species tree for GeneRax.


## TODOs  
- add the scripts for a tree cleaning for GeneRax  
- check the alignments that have failed    


Get a tree from NCBI:  
`species_prefixes.tab` has a form: 

```
[PREFIX,e.g Mmus]\t[NAME,e.g. Mus musculus]
```  

# NCBI tree   

Fetch the tree for your species using NCBI:  


```bash
cat species_prefixes.tab | grep -f species_list | cut -f 2 | sort | uniq > ids
python ncbi_tree.py --input ids --prefixes species_prefixes.tab > test.tree
python plot.py test.tree test.pdf
```


# BUSCO tree   


Launch the job:  

```bash
mamba activate phylo
sbatch --mem=10G --time=06:00:00 submit.sh 
```

The job launched:  
```bash
BUSCODIR=/users/asebe/xgraubove/genomes/annotation_busco/ # path to Xavi's busco analysis directory
IQTREE=/users/xgraubove/Programes/iqtree-2.1.0-Linux/bin/iqtree2

python busco_tree.py --busco_dir $BUSCODIR --iqtree $IQTREE --species_list species_list --fmin 1 --ncpu 4
python reroot.py --input results_busco/supermatrix.treefile --outgroup Cowc > results_busco/supermatrix.roooted.treefile
python plot.py results_busco/supermatrix.roooted.treefile output.pdf
```
