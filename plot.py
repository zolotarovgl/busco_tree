#!/usr/bin/env python3
import os
os.environ["QT_QPA_PLATFORM"] = "offscreen"
from ete3 import Tree

from ete3 import Tree
import sys

if len(sys.argv) < 2:
    print("Usage: pretty_tree.py treefile [output.pdf]")
    sys.exit(1)

treefile = sys.argv[1]
t = Tree(treefile)
print(t.get_ascii(show_internal=True))

if len(sys.argv) > 2:
    outfile = sys.argv[2]
    t.render(outfile, w=600, units="mm")
    print(f"Tree saved to {outfile}")

