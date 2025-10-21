ID=$1
echo $ID
cat tmp/*single_copy | grep $ID > tmp/aln.${ID}.fofn
cat $(cat tmp/aln.${ID}.fofn) > tmp/aln.${ID}.fasta
mafft --quiet --maxiterate 1000 --oldgenafpair tmp/aln.${ID}.fasta > tmp/aln.${ID}.l.fasta

# rename the sequnces:
bioawk -c fastx -v ID=$ID '{split($name,a,"_");print ">"a[1]"_"ID"\n"$2}' tmp/aln.$ID.l.fasta > tmp/aln.$ID.l.fasta.tmp
mv tmp/aln.$ID.l.fasta.tmp tmp/aln.$ID.l.fasta
