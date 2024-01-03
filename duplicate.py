import sys

if len(sys.argv) != 2:
    print("You need to provide 1 (and only 1) input file")
    exit()

filename = sys.argv[1]
file = open(filename)

# Read the file and count the occurrence of line
line_freq = dict()
for line in file:
    line = line.strip()
    line_freq.setdefault(line, 0)
    line_freq[line] += 1
file.close()

output1 = open(filename + "_duplicate", "w")
output2 = open(filename + "_unique", "w")

for key in line_freq:
    value = line_freq[key]
    # Print the duplicates
    if value > 1:
        for i in range(value - 1):
            output1.write(key + "\n")

    # Print the unique value of lines
    output2.write(key + "\n")

output1.close()
output2.close()
