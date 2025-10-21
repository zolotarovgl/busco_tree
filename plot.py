#!/usr/bin/env python3
import os, sys
os.environ["QT_QPA_PLATFORM"] = "offscreen"
from ete3 import Tree, TreeStyle, NodeStyle, TextFace

if len(sys.argv) < 2:
    print("Usage: pretty_tree.py treefile [output.pdf]")
    sys.exit(1)

t = Tree(sys.argv[1])

print(t.get_ascii(show_internal=True))

if len(sys.argv) > 2:
    outfile = sys.argv[2]
    ts = TreeStyle()
    ts.mode = "r"
    ts.force_topology = True
    ts.show_leaf_name = False
    ts.show_branch_length = False  # ← hides numeric lengths
    ts.show_branch_support = True
    ts.branch_vertical_margin = 5  # balanced spacing per leaf
    ts.optimal_scale_level = "mid"

    for n in t.traverse():
        ns = NodeStyle()
        ns["size"] = 0
        ns["vt_line_width"] = 1
        ns["hz_line_width"] = 1
        n.set_style(ns)
        if n.is_leaf():
            n.add_face(TextFace(n.name, fsize=7), column=0, position="branch-right")
        elif n.name:
            n.add_face(TextFace(n.name, fsize=5, fgcolor="gray"), column=0, position="branch-top")

    # dynamic height: ~6 mm per leaf for font size 7
    h_mm = max(50, len(t) * 10)
    t.render(outfile, w=180, h=h_mm, units="mm", tree_style=ts)
    print(f"Tree saved to {outfile}")

