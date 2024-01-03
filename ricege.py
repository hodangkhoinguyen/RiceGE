import urllib.request
import argparse
import os

# Mutants that are in RiceGE
def get_current_ricege(url) -> set:
    file = urllib.request.urlopen(url)
    mutant_ricege_set = set()
    for line in file:
        line = line.decode("utf-8")
        parsing_line = line.split("\t")
        mutant = parsing_line[0].split(".")[0]
        mutant_ricege_set.add(mutant)
    return mutant_ricege_set

# Mutants that are in the browse table
def get_browse_table(filename):
    browse_file = open(filename)
    mutant_dict = {}
    for line in browse_file:
        parsing_line = line.strip().split("\t")
        sno = parsing_line[0]
        mutant = parsing_line[1]
        generation = parsing_line[2]
        mutations = parsing_line[3]
        genes = parsing_line[4]
        weights = int(parsing_line[5])
        availability = "Yes" if weights > 0 else "No"
        mutant_dict[mutant] = f"SNo: {sno}, Mutant_ID: {mutant}, Generation: {generation}, Mutations: {mutations}, Genes: {genes}, Seed availability: {availability}"
    browse_file.close()
    return mutant_dict

# Read the mutant gene table file
def get_ricege_output(mutant_gene_filename: str, mutant_type: str, mutant_dict: dict, mutant_set: set):
    gene_file = open(mutant_gene_filename)
    mutant_gene_dict = {}
    not_found_set = set()
    ricege_mutant_type = mutant_type
    if mutant_type == "Single Base Substitution":
        ricege_mutant_type = "SNP" 
    for line in gene_file:
        parsing_line = line.strip().split("\t")
        mutant = parsing_line[0]
        chrom = parsing_line[3]
        chrom_num = chrom[3:]
        start = parsing_line[4]
        end = parsing_line[5]
        mut_type = parsing_line[9]
        mut_size = parsing_line[10]
        if len(parsing_line) >= 14:
            gene_name = parsing_line[13]
        else:
            gene_name = ""

        if len(parsing_line) >= 15:
            gene_desc = parsing_line[14]
        else:
            gene_desc = ""
        if mutant not in mutant_set:
            continue

        if mut_type != mutant_type:
            continue

        # Key for mutant_gene_dict: mutant_id.mutant_type.chrom.start_position
        id = f"{mutant}.{ricege_mutant_type[:3]}.{chrom_num}:{start}"
        if mutant not in mutant_dict.keys():
            not_found_set.add(mutant)
            continue

        if id not in mutant_gene_dict.keys():
            mutant_gene_dict[id] = [
                id,
                f"chr{chrom_num.rjust(2, '0')}:{start.rjust(9, '0')}",
                "0",
                f"W/{start}-{end}",
                f"{mutant} {mutant_type} {mut_size}", 
                [], # Gene info - index 5
                mutant_dict[mutant]
            ]

        # Add gene info
        if f"{gene_name} {gene_desc}" not in mutant_gene_dict[id][5]:
            mutant_gene_dict[id][5].append(f"{gene_name} {gene_desc}")

    output_filename = f"ricege_{ricege_mutant_type}"
    output = open(output_filename, "w")
    for id in mutant_gene_dict.keys():
        writeline = "\t".join(mutant_gene_dict[id][:5])
        writeline += " " + ", ".join(mutant_gene_dict[id][5]) # append gene info
        writeline += (" " + mutant_gene_dict[id][6] + "\n") # append mutant info from browse table
        output.write(writeline)

    gene_file.close()
    output.close()
    return output_filename

def main():
    parser = argparse.ArgumentParser(description = "Produce RiceGE format from browse table and mutant gene table")
    parser.add_argument('--browse', type=str, required=True, help="browse table file name")
    parser.add_argument('--file', type=str, required=True, help="mutant gene table file name")
    parser.add_argument('--type', type=str, required=True, help="mutant type", choices = ["Deletion", "Insertion", "Inversion", "SNP", "Translocation"])
    parser.add_argument('--prev', type=str, choices = ["yes", "no"], help="create RiceGE database that are not in previous RiceGE")

    args = parser.parse_args()
    mutant_type = args.type
    check_prev = args.prev != None and args.prev == "yes"

    mutant_dict = get_browse_table(args.browse)
    mutant_set = set(mutant_dict.keys())

    if check_prev:
        url = f"http://signal.salk.edu/database/RiceGE7/Kitaake.mutants.{mutant_type}.v7"
        mutant_ricege_set = get_current_ricege(url)
        mutant_set = mutant_set - mutant_ricege_set

    if mutant_type == "SNP":
        mutant_type = "Single Base Substitution"

    output_name = get_ricege_output(args.file, mutant_type, mutant_dict, mutant_set)
    os.system(f"sort -k2 {output_name} > {output_name}_sorted")

if __name__ == '__main__':
    main()
