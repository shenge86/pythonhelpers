infile = "input.txt"
outfile = "output.txt"
with open(infile) as fin, open(outfile, "w+") as fout:
    for line in fin:
        line = line.strip()
        #line = ",".join(line.split())
        #line = ' '.join(line.split(',')[0:4]) + ','.join(line.split(',')[4:])
        line = ' '.join(line.split()[0:4]) + ','.join(line.split()[4:])
        line += '\n'
        print(line)
        fout.write(line)
