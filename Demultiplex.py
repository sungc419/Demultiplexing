#!/usr/bin/env python

import argparse
import gzip
import bioinfo
import itertools 

def get_args():
    parser = argparse.ArgumentParser(description = "A program for demultiplexing 4 FASTQ input files given a list of barcodes")
    parser.add_argument("-i", "--i_file", help="index input file", required=True)
    parser.add_argument("-R1", "--R1_file", help="R1 input file", required=True)
    parser.add_argument("-R2", "--R2_file", help="R2 input file", required=True)
    parser.add_argument("-R3", "--R3_file", help="R3 input file", required=True)
    parser.add_argument("-R4", "--R4_file", help="R4 input file", required=True)
    return parser.parse_args()

args = get_args()
i_file = args.i_file
R1 = args.R1_file
R2 = args.R2_file
R3 = args.R3_file
R4 = args.R4_file

i_set = set() # initialize empty set to store list of 24 indices

with open ("/projects/bgmp/shared/2017_sequencing/indexes.txt", "r") as f_i: # open file with list of 24 indices from Talapas
    for line in f_i: # loop over each line
        if not line.startswith("sample"): # remove header
            columns = line.strip().split('\t') # create a list of each column in file and remove newline character
            columns_seq = columns[4] # extract only the sequence from column 5 in each line (returns str)
            i_set.add(columns_seq) # add each extracted sequence to the empty set

count_dict = {} # initialize empty dictionary to store barcode combinations as keys and their count as values
combo_list = list(itertools.combinations_with_replacement(i_set, 2))

for barcode in combo_list:
    item1 = barcode[0] # first item in tuple
    item2 = barcode[1] # second item in tuple
    combo = f'{item1}-{item2}'
    count_dict[combo] = 0

f_dict = {} # initialize empty dictionary to store barcodes as keys and writable output filenames as values 

h_R1 = open("output/hopped_R1.fq","w") # create filename for writing hopped output file
h_R2 = open("output/hopped_R2.fq","w")
un_R1 = open("output/unknown_R1.fq","w") # create filename for writing unknown output file
un_R2 = open("output/unknown_R2.fq","w")

for i in i_set: # create empty output files
    f_dict[i] = [open(f'output/{i}_R1.fq', "w"), open(f'output/{i}_R2.fq', "w")] 


# R1="/projects/bgmp/csung/bioinfo/Bi622/Demultiplexing/TEST-input_FASTQ/test_R1.fq"
# R2="/projects/bgmp/csung/bioinfo/Bi622/Demultiplexing/TEST-input_FASTQ/test_R2.fq"
# R3="/projects/bgmp/csung/bioinfo/Bi622/Demultiplexing/TEST-input_FASTQ/test_R3.fq"
# R4="/projects/bgmp/csung/bioinfo/Bi622/Demultiplexing/TEST-input_FASTQ/test_R4.fq"

unknown = 0
hopped = 0

with gzip.open(R1, "rt") as fR1, gzip.open(R2, "rt") as fR2, gzip.open(R3,"rt") as fR3, gzip.open(R4,"rt") as fR4:
    while True:
        rec1 = bioinfo.read_fqrec(fR1) # creates list of each line in record
        rec2 = bioinfo.read_fqrec(fR2)
        rec3 = bioinfo.read_fqrec(fR3)
        rec4 = bioinfo.read_fqrec(fR4)

        if rec1[0] == "":
            break

        # print(rec1)
        # print(rec2)
        # print(rec3)
        # print(rec4)

        rec3[1] = bioinfo.rev_comp(rec3[1])

        seq2 = rec2[1]
        seq3 = rec3[1]

        if (seq2 not in i_set) or (seq3 not in i_set):
            unknown += 1 # count number of unknown pairs
            un_R1.write(f'{rec1[0]} {seq2}-{seq3}\n{rec1[1]}\n{rec1[2]}\n{rec1[3]}\n') # write out to unknown R1 file
            un_R2.write(f'{rec4[0]} {seq2}-{seq3}\n{rec4[1]}\n{rec4[2]}\n{rec4[3]}\n') # write out to unknown R2 file
        elif seq2 == seq3:        
            combo = f'{seq2}-{seq3}'
            count_dict[combo] += 1
            fhR1, fhR2 = f_dict[seq2] # tuple unpacking of output file list
            fhR1.write(f'{rec1[0]} {seq2}-{seq3}\n{rec1[1]}\n{rec1[2]}\n{rec1[3]}\n') # write out to unknown R1 file
            fhR2.write(f'{rec4[0]} {seq2}-{seq3}\n{rec4[1]}\n{rec4[2]}\n{rec4[3]}\n') # write out to unknown R2 file
        else: 
            hopped += 1 # count number of hopped pairs
            h_R1.write(f'{rec1[0]} {seq2}-{seq3}\n{rec1[1]}\n{rec1[2]}\n{rec1[3]}\n') # write out to hopped R1 file
            h_R2.write(f'{rec4[0]} {seq2}-{seq3}\n{rec4[1]}\n{rec4[2]}\n{rec4[3]}\n') # write out to hopped R2 file
