# RiceGE Database Conversion

From the most current mutant gene table and browse table of Nipponbare, we convert them into RiceGE database format. Before running the script to get RiceGE format, you need to export the browse table and mutant gene table from MySQL tables into text/tsv/csv files (no header lines). Examples for these 2 files can be found under [examples](./examples/).

# How to run

`dupilcate.py` is to check the duplicated rows in a file. You need to provide a filename as argument.

```
python3 duplicate.py <filename>
```

`browse_table.py` is to produce a browse table file from mutant gene table file. You need to provide input and output filenames.

```
python3 browse_table.py <input_name> <output_name>
```

`ricege.py` is to produce a RiceGE format file from browse table and mutant gene table files. You need to provide 2 files above, mutant type, and whether you want to run all mutants or just mutants that are NOT in the previous RiceGE version that is available [here](http://signal.salk.edu/database/RiceGE7/).

```
python3 --browse <browse_table> --file <mutant_gene_table> --type <mut_type> --prev <yes/no>
```

Mutant type options: Deletion, Insertion, Inversion, SNP, Translocation.
By default, `--prev` is optional and automatically `no`, which will produce ALL mutants. Using `yes` will take previous mutant in RiceGE into account to avoid duplicates.
