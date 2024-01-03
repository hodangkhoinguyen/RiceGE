import sys
import re

if len(sys.argv) != 3:
    print("You need to include 1 input file as mutant gene table and another filename for output")
    exit()

combine_file = open(sys.argv[1])

# Define column index
MUTANT_ID = 0
CHROM_NUM = 2
START_POS = 3
END_POS = 4
CHROM_NUM2 = 5
START_POS2 = 6
END_POS2 = 7
MUT_TYPE = 8
MUT_SIZE = 9
GENE_NAME = 13

# Create a mutant dictionary to keep track of their mutant lines and genes
mutant_dict = {}

for line in combine_file:
    if line.startswith('mutant_id'):
        continue

    parsingLine = line.split('\t')
    mutant_id = parsingLine[MUTANT_ID]

    # Doesn't have gene
    if len(parsingLine) <= GENE_NAME:
        gene = ''
    else:
        gene = parsingLine[GENE_NAME].strip()

    mutant_dict.setdefault(mutant_id, {
        'lines': set(),
        'genes': set(),
        'num_list': re.findall(r'\d+' , mutant_id)
    })

    mutant_dict[mutant_id]['lines'].add(parsingLine[MUTANT_ID] + "\t" + "\t".join(parsingLine[CHROM_NUM:(MUT_SIZE+1)]))
    if gene != '' and gene.startswith('LOC'):
        if gene.startswith('LOC'):
            mutant_dict[mutant_id]['genes'].add(gene)
        else:
            print("This gene is strange:", gene)

combine_file.close()

def compare_num_list(list1, list2):
    i = 0
    while i < len(list1) and i < len(list2):
        num1 = int(list1[i])
        num2 = int(list2[i])
        if num1 > num2:
            return 1
        elif num1 < num2:
            return -1
        i += 1

    if len(list1) > len(list2):
        return 1
    elif len(list1) == len(list2):
        return 0
    return -1

# Add missing mutant ID
mutant_dict.setdefault('FN-57', {
        'lines': set(),
        'genes': set(),
        'num_list': re.findall(r'\d+' , 'FN-57')
    })

# Sort dictionary by number in the mutant ID
result_list = []

for mutant_id in mutant_dict:
    value =  mutant_dict[mutant_id]
    num_list = value['num_list']
    isAdded = False
    for j in range(len(result_list)):
        _, curr_num_list = result_list[j]

        if compare_num_list(num_list, curr_num_list) < 0:
            result_list.insert(j, (mutant_id, num_list))
            isAdded = True
            break
    if not isAdded:
        result_list.append((mutant_id, num_list))

old_browse_dict = dict()
old_browse_file = open('browse-table-2023.tsv')
for line in old_browse_file:
    parsingLine = line.strip().split('\t')
    mutant_id = parsingLine[1]
    gen = parsingLine[2]
    weight = parsingLine[5]
    old_browse_dict[mutant_id] = {
        'gen': gen,
        'weight': int(weight)
    }
old_browse_file.close()

output_file = open(sys.argv[2], "w")

sno = 1
for id, _ in result_list:
    old_value = old_browse_dict.get(id)
    if old_value == None:
        gen = "M2"
        weight = 1
    else:
        gen = old_browse_dict[id]['gen']
        weight = old_browse_dict[id]['weight']
        if weight > 0:
            weight = 1

    # Writing line with the format mutant_id generation number_mutants number_genes weights (weight default by 1)
    line = f"{sno}\t{id}\t{gen}\t{len(mutant_dict[id]['lines'])}\t{len(mutant_dict[id]['genes'])}\t{weight}\n"
    output_file.write(line)
    sno += 1
output_file.close()
