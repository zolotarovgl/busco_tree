#!/usr/bin/env python3
import argparse
from ete3 import NCBITaxa
import sys

parser = argparse.ArgumentParser(description = "Given a list of species names, gather a tree from NCBI")
parser.add_argument("--input", required=True, help="File with species list")
parser.add_argument("--prefixes", help="Optional tab-delimited file: prefix<TAB>species_name")
args = parser.parse_args()

with open(args.input) as f:
    names = [line.strip().replace("_", " ") for line in f if line.strip()]

prefix_map = {}
if args.prefixes:
    with open(args.prefixes) as pf:
        for line in pf:
            if not line.strip():
                continue
            prefix, species = line.strip().split("\t", 1)
            prefix_map[species.replace("_", " ")] = prefix
ncbi = NCBITaxa()
taxids = []
name_to_taxid = {}
for n in names:
    try:
        taxid = ncbi.get_name_translator([n])[n][0]
        taxids.append(taxid)
        name_to_taxid[taxid] = n
    except KeyError:
        continue
        #print(f"Warning: species '{n}' not found in NCBI, skipping.")

if not taxids:
    print("Error: no valid species found.")
    exit(1)

tree = ncbi.get_topology(taxids)
all_taxids = [int(n.name) for n in tree.traverse()]
translator = ncbi.get_taxid_translator(all_taxids)

for node in tree.traverse():
    tid = int(node.name)
    node.dist = 0  # remove branch length
    if tid in translator:
        name = translator[tid]
        if node.is_leaf():
            if name in prefix_map:
                node.name = prefix_map[name]
            else:
                print(f'ERROR: {name} not found in the prefix file!')
                sys.exit(1)
                #node.name = name
        else:
            node.name = translator[tid].replace(" ", "_")

#print(tree.write(format=1))
print(tree.write(format=9))
