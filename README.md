## Dump contigs from Ensembl REST to BED file

### E.g. dump Human contigs and generate BigBED
Assumes Kent utils are available
```
python dump_contigs.py Human > human_contigs.bed

bedSort human_contigs.bed human_contigs_sorted.bed

fetchChromSizes hg38 > hg38.chrom.sizes
sed -i 's/chr//' hg38.chrom.sizes
echo -e "MT\t16569" >> hg38.chrom.sizes

bedToBigBed -type=bed6 human_contigs_sorted.bed hg38.chrom.sizes human_contigs_sorted.bb
```
