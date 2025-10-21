#!/usr/bin/env python3
import sys
import os
import subprocess
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Run BUSCO-based supermatrix alignment and tree inference")
parser.add_argument("--busco_dir", required=True, help="Directory containing BUSCO results")
parser.add_argument("--species_list", required=True, help="File with species names, one per line")
parser.add_argument("--iqtree", required=True, help="Path to iqtree2 binary")
parser.add_argument("--ncpu", type=int, default=1, help="Number of CPUs")
parser.add_argument("--fmin", type=float, default=float(0.7), help="Minimum fraction of species per BUSCO to include. Default: 0.7")
args = parser.parse_args()

busco_dir = Path(args.busco_dir)
tmp_dir = Path("tmp")
res_dir = Path("results_busco")
tmp_dir.mkdir(exist_ok=True)
res_dir.mkdir(exist_ok=True)
subprocess.run(["mkdir", "-p", "tmp_parallel"], check=True)
os.environ["TMPDIR"] = "tmp_parallel"


# Prepare species patterns
species_pats = tmp_dir / "species_pats"
with open(args.species_list) as f, open(species_pats, "w") as out:
    for line in f:
        out.write(f"_{line.strip()}_\n")

# Find BUSCO folders
busco_fofd = tmp_dir / "busco_fofd"
cmd = f"paste <(find {busco_dir} -maxdepth 1 -type d | grep -f {species_pats} -o) " \
      f"<(find {busco_dir} -maxdepth 1 -type d | grep -f {species_pats}) | " \
      f"awk '!seen[$1]++ {{print $2}}' > {busco_fofd}"
subprocess.run(["bash","-c",cmd], check=False)

nf = int(subprocess.getoutput(f"wc -l {busco_fofd} | cut -f1 -d' '"))
ns = int(subprocess.getoutput(f"wc -l {species_pats} | cut -f1 -d' '"))
print(f"Found {nf}/{ns} BUSCO results in {busco_dir}")

if nf < ns:
    print(f"ERROR: missing species!")
    sys.exit(1)


# Create per-species single-copy lists
for line in open(busco_fofd):
    l = line.strip()
    if not l:
        continue
    sps = Path(l).name.split("_")[1]
    target = tmp_dir / f"{sps}.single_copy"
    cmd = f"find {l}/run_metazoa_odb10/busco_sequences/single_copy_busco_sequences -name '*faa' | sort > {target}"
    subprocess.run(["bash","-c",cmd], check=False)

# Select single-copy BUSCOs with enough species
nmin = int(float(args.fmin) * nf)
print(f'fmin: {args.fmin}\nnmin: {nmin}')


torun = tmp_dir / "single_copy_torun"
cmd = f"cat {tmp_dir}/*single_copy | awk -F'/' '{{print $NF}}' | sed 's/.faa//g' | " \
      f"sort | uniq -c | awk -v NMIN={nmin} '$1>=NMIN {{print $2i}}' > {torun}"
subprocess.run(["bash","-c",cmd], check=False)
n = int(subprocess.getoutput(f"wc -l {torun} | cut -f1 -d' '"))
print(f"{n} single-copy orthologs found in at least {nmin} species.")
nmax = 1000
args.ncpu = min(int(args.ncpu),nmax)
if n==0:
    print(f"ERROR: no busco copies present in at least {nmin} / {nf} species!")
    sys.exit(1)
elif n > nmax:
    print(f"WARNING: number of orthologs is higher {n} than allowed {nmax}, selecting randomly!") 
    cmd = ["bash","-c",f"cat {torun} | shuf -n {nmax} | parallel -j {args.ncpu} 'bash align_busco.sh {{}}'"]
else:
    cmd = ["bash","-c",f"cat {torun} | parallel -j {args.ncpu} 'bash align_busco.sh {{}}'"]

# Run alignments
subprocess.run(cmd)
# Add missing species sequences
for f in tmp_dir.glob("aln.*.l.fasta"):
    cmd = f"""
    awk -v ID={os.path.splitext(os.path.basename(f))[0]} 'FNR==NR {{ species_list[$1]+=1; next }}
    {{ alnlen = length($2); split($1,a,"_"); sp_seen[a[1]]+=1; print ">"$1"\\t"$2 }}
    END {{
        for (sp in species_list) {{
            if (!(sp in sp_seen)) {{
                emptyseq = gensub(/ /, "-", "g", sprintf("%*s", alnlen, ""));
                print ">"sp"_"ID"\\t"emptyseq
            }}
        }}
    }}' {args.species_list} <(bioawk -c fastx '{{print $0}}' {f}) | sort -k 1 | \
    awk '{{print $1"\\n"$2}}' > {f}.tmp && mv {f}.tmp {f}
    """

    subprocess.run(["bash", "-c", cmd], check=True)



# Concatenate alignments
cmd = (
    f"cat {tmp_dir}/aln.*.l.fasta | bioawk -c fastx '{{print $0}}' | "
    "awk '{split($1,a,\"_\");species=a[1];seqs[species]=seqs[species]\"\"$2}"
    "END{for(k in seqs){print \">\"k\"\\n\"seqs[k]}}' > results_busco/supermatrix.fa"
)
subprocess.run(["bash","-c",cmd], check=False)

# Run ClipKit
subprocess.run([
    "clipkit",
    "results_busco/supermatrix.fa",
    "-m","kpic-gappy",
    "-o","results_busco/supermatrix.t.fa",
    "-g","0.7"
], check=False)

# Run IQ-TREE
subprocess.run([
    args.iqtree,
    "-s","results_busco/supermatrix.t.fa",
    "-m","TEST",
    "-mset","LG,WAG,JTT",
    "-nt","AUTO",
    "-ntmax",str(args.ncpu),
    "-bb","1000",
    "-pre","results_busco/supermatrix",
    "-nm","10000",
    "-nstop","200",
    "-cptime","1800"
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)

