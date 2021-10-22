#infile = "input/comms/IM2/Chain1_Chronological.txt"
#outfile = "output/comms/IM2/Chain1_Chronological_done.txt"
#delete_list = ["Facility/", "To Satellite/IM2_DRM1_8_1"]

infile = "input/boresight.txt"
outfile = "output/boresight.txt"

delete_list = ["{", "}", "'", "array(", "),"]
with open(infile) as fin, open(outfile, "w+") as fout:
    for line in fin:
        for word in delete_list:
            line = line.replace(word, "")
        fout.write(line)
