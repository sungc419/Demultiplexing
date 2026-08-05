#!/usr/bin/env python

# Author: <YOU> <optional@email.address>

# Check out some Python module resources:
#   - https://docs.python.org/3/tutorial/modules.html
#   - https://python101.pythonlibrary.org/chapter36_creating_modules_and_packages.html
#   - and many more: https://www.google.com/search?q=how+to+write+a+python+module

'''This module is a collection of useful bioinformatics functions
written during the Bioinformatics and Genomics Program coursework.
You should update this docstring to reflect what you would like it to say'''

__version__ = "0.3"         # Read way more about versioning here:
                            # https://en.wikipedia.org/wiki/Software_versioning

from typing import TextIO

DNA_bases = set('ATGCNatcgn')
RNA_bases = set('AUGCNaucgn')

def convert_phred(letter: str) -> int:
    '''Converts a single character into a phred score'''
    return ord(letter) - 33

def qual_score(phred_score: str) -> float:
    """This calculates the average quality score of the whole phred string."""
    phred_sum = 0
    for x in phred_score:
        phred_sum += convert_phred(x) 
    return phred_sum / len(phred_score)

def validate_base_seq(seq,RNAflag=False):
    '''This function takes a string. Returns True if string is composed
    of only As, Ts (or Us if RNAflag), Gs, Cs. False otherwise. Case insensitive.'''
    seq = seq.upper()
    seq = set (seq)
    return seq <= (RNA_bases if RNAflag else DNA_bases)

def gc_content(DNA):
    '''This function calculates the GC content of a DNA sequence.'''
    assert validate_base_seq(DNA)
    DNA = DNA.upper()
    return (DNA.count("G") + DNA.count("C")) / len(DNA)

def calc_median(lst):
    '''Given a sorted list, returns the median value of the list'''
    n = len(lst)
    if n % 2 == 0:
        med = (lst[(n//2)-1] + lst[n//2])/2
    else:
        med = lst[n//2]     
    return med

def oneline_fasta(file_i, file_o):
    '''Writes all sequences in a FASTA file to one line per record.'''
    with open (file_i, "r") as f_i, open(file_o, "w") as f_o:
        for l, line in enumerate(f_i):
            line = line.strip("\n")
            if not line.startswith(">"):
                f_o.write(line)
            else: 
                if l ==0:
                    f_o.write(f'{line}\n')
                else:
                    f_o.write(f'\n{line}\n')

dna_dict = {'A': 'T', 'G': 'C', 'C':'G', 'T':'A', 'N':'N'}

def rev_comp(seq: str) -> str:
    ''' Takes the dna sequence (string) and returns the reverse complement. Base of N should return N.''' 
    seq = seq.upper()
    rev = seq[::-1]
    comp = "" 
    for base in rev:
        print(base)
        comp += dna_dict[base] 
    return comp


def read_fqrec(fh: TextIO)-> list: 
    '''Takes a FASTQ file and stores the 4 lines in each record in a list, stripping newline characters'''
    record = []
    for i in range(4):
        record.append(fh.readline().strip())
    return record


if __name__ == "__main__":
    # write tests for functions above, Leslie has already populated some tests for convert_phred
    # These tests are run when you execute this file directly (instead of importing it)
    assert convert_phred("I") == 40, "wrong phred score for 'I'"
    assert convert_phred("C") == 34, "wrong phred score for 'C'"
    assert convert_phred("2") == 17, "wrong phred score for '2'"
    assert convert_phred("@") == 31, "wrong phred score for '@'"
    assert convert_phred("$") == 3, "wrong phred score for '$'"
    print("Your convert_phred function is working! Nice job")

    assert qual_score("FFF") == 37
    assert qual_score("?M") == 37
    assert qual_score("KO") == 44
    print("You calculated the correct average phred score")

    assert validate_base_seq("AGTAGGG", False) == True, "Validate base seq does not work on DNA"
    assert validate_base_seq("GAUAAUUUUUU", True) == True, "Validate base seq does not work on RNA"
    assert validate_base_seq("UCTATTU", False) == False
    assert validate_base_seq("CUUCUGGG", False) == False
    print("Passed DNA and RNA tests")

    assert gc_content("GC") == 1
    assert gc_content("TATATA") == 0
    assert gc_content("CGAT") == 0.5
    print("correctly calculated GC content")

    assert calc_median([1,3,5,7,9]) == 5, "calc_median function does not work for odd length list"
    assert calc_median([3,4]) == 3.5, "calc_median function does not work for even length list"
    assert calc_median([2,2,2,2,2,2,2,1000]) == 2
    assert calc_median([2,3,4,5,6,7,8,9]) == 5.5
    print("Median successfully calculated")

