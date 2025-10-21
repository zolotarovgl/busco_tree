#!/usr/bin/env python3
from ete3 import Tree
import argparse

parser = argparse.ArgumentParser(description="Reroot a Newick tree using one or more outgroup taxa.")
parser.add_argument("--input", required=True, help="Input Newick tree file")
parser.add_argument("--outgroup", required=True, help="Comma-separated list of outgroup taxa (e.g. 'Mbre,Sros')")
args = parser.parse_args()

t = Tree(args.input)
outgroup_taxa = [x.strip() for x in args.outgroup.split(",")]

if len(outgroup_taxa) == 1:
    t.set_outgroup(t & outgroup_taxa[0])
else:
    mrca = t.get_common_ancestor(outgroup_taxa)
    t.set_outgroup(mrca)

print(t.write(format=9))
