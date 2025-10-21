#!/usr/bin/env python3
import os
os.environ["QT_QPA_PLATFORM"] = "offscreen"
from ete3 import TreeStyle, TextFace
from ete3 import Tree
import sys

if len(sys.argv) < 2:
    print("Usage: pretty_tree.py treefile [output.pdf]")
    sys.exit(1)

treefile = sys.argv[1]
t = Tree(treefile)
print(t.get_ascii(show_internal=True))
from ete3 import TreeStyle, TextFace, NodeStyle

if len(sys.argv) > 2:
    outfile = sys.argv[2]
    ts = TreeStyle()
    ts.show_leaf_name = False  # disable default labels
    ts.show_branch_length = False
    ts.show_branch_support = False
    ts.scale = 120
    ts.branch_vertical_margin = 10
    for n in t.traverse():
        if n.is_leaf():
            ns = NodeStyle()
            ns["size"] = 0
            n.set_style(ns)
            n.add_face(TextFace(n.name, fsize=7), column=0, position="branch-right")
    t.render(outfile, w=600, units="mm", tree_style=ts)
    print(f"Tree saved to {outfile}")
