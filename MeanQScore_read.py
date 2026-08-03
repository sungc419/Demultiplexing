#!/usr/bin/env python

import argparse
import matplotlib.pyplot as plt
import bioinfo
import gzip

def get_args():
    parser = argparse.ArgumentParser(description = "A program for averaging quality scores at each position given 4 FASTQ input files R1(read1), R2(index1), R3(index2), R4(read2)")
    parser.add_argument("-f", "--in_file", help="input file")
    parser.add_argument("-r", "--fname", help="file name for png")
    return parser.parse_args()

args = get_args()
in_file = args.in_file
fname = args.fname


def init_list(lst: list, value: float=0.0) -> list:
    '''This function takes an empty list and will populate it with the value passed in "value". If no value is passed, initializes list with 101 values of 0.0.'''
    for x in range(101):
        lst.append(value)
    return lst

my_list: list = []
my_list = init_list(my_list)

def populate_list(file: str) -> tuple[list, int]: 
    #write docstring anytime you define a new function
    """This function opens a FASTQ file and uses two counters to add the sum of the Phred scores in every fourth line of the file at each base position. One counter tracks the total number of lines in the file and the other tracks the base position in each line. It then calls on a function stored in the bioinfo module to convert the Phred scores. A list of 101 values of quality score sums at each base and the total number of rows in the file is returned at the end.""" 
    
    lst = init_list([])  # use empty list to not add another set of 0.0s
    with gzip.open(in_file, 'rt') as fh: # opens FASTQ file
        line_num = 0 # starts with 0 line number
        for line in fh: # loops over each line in the file
            line_num += 1   # counter for keeping track of total number of lines in the file
            line = line.strip("\n") # strips the newline character
            if line_num %4 == 0: # filters for every 4th line in the file
                ntnum = -1 # start with base position of -1 to start with position 0 
                for nt in line: # loops over each base in each 4th line
                    ntnum += 1  # counter for keeping track of nucleotide number
                    lst[ntnum] += bioinfo.convert_phred(nt) # populates new list of 101 values with converted phred score 
    return lst, line_num

my_list, num_lines = populate_list(in_file)

for nt_pos in range(len(my_list)): #nt_pos = nucleotide position
    my_list[nt_pos] = my_list[nt_pos]/(num_lines/4)

x = range(nt_pos+1)
y = my_list

plt.bar(x, y)
plt.title(f'Mean Quality Score at Each Base for {fname}')
plt.xlabel('Base Position')
plt.ylabel('Mean Quality Score')
plt.savefig(f'{fname}.png')