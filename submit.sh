#!/bin/bash
#SBATCH --job-name=busco_tree
#SBATCH --output=log_%j.out
#SBATCH --error=log_%j.err
#SBATCH --cpus-per-task=32
#SBATCH --mem=1G

BUSCODIR=/users/asebe/xgraubove/genomes/annotation_busco/
IQTREE=/users/asebe/xgraubove/Programes/iqtree-2.1.0-Linux/bin/iqtree2

python busco_tree.py \
    --busco_dir "$BUSCODIR" \
    --iqtree "$IQTREE" \
    --species_list species_list \
    --fmin 0.7 \
    --ncpu 32

python plot.py results_busco/supermatrix.treefile output.pdf
echo "done"
