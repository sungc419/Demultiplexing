# Demultiplex Assignment for Bi622

**7/30/2026 Initial data exploration:**

Determine which files contain the indexes, and which contain the paired end reads containing the biological data of interest. Create a table and label each file with either read1, read2, index1, or index2.

Files are located in Talapas:
```/projects/bgmp/shared/2017_sequencing/```

These are the files of interest:

```
1294_S1_L008_R1_001.fastq.gz  1294_S1_L008_R3_001.fastq.gz     indexes.txt
1294_S1_L008_R2_001.fastq.gz  1294_S1_L008_R4_001.fastq.gz
```

Comparing the first few sequences of R2 vs R3:

```zcat 1294_S1_L008_R2_001.fastq.gz | head -40```
```zcat 1294_S1_L008_R3_001.fastq.gz | head -40```

1st sequence of each file: NCTTCGAC (R2) vs NTCGAAGA (R3)
2nd sequence of each file: NACAGCGA (R2) vs NCGCTGTT (R3)
3rd sequence of each file: NTCCTAAG (R2) vs NTTAGGAC (R3)

R2 is the forward read and R3 is the reverse complement. 

Comparing R1 vs R4:

```zcat 1294_S1_L008_R1_001.fastq.gz | head -40```
```zcat 1294_S1_L008_R4_001.fastq.gz | head -40```

1st sequence:
GNCTGGCATTCCCAGAGACATCAGTACCCAGTTGGTTCAGACAGTTCCTCTATTGGTTGACAAGGTCTTCATTTCTAGTGATATCAACACGGTGTCTACAA  (R1)

NTTTTGATTTACCTTTCAGCCAATGAGAAGGCCGTTCATGCAGACTTTTTTAATGATTTTGAAGACCTTTTTGATGATGATGATGTCCAGTGAGGCCTCCC  (R4)

2nd sequence:
CNACCTGTCCCCAGCTCACAGGACAGCACACCAAAGGCGGCAACCCACACCCAGTTTTACAGCCACACAGTGCCTTGTTTTACTTGAGGACCCCCCACTCC  (R1)

NTGTGTAGACAAAAGTTTTCATGAGTCTGTAAGCTGTCTATTGTCTCCTGAAAAGAAACCAGAAGTTTTCCCCTAAATGTGTTTAGAATGCTTATTCTAAT  (R4)

3rd sequence:
GNGGTCTTCTACCTTTCTCTTCTTTTTTGGAGGAGTAGAATGTTGAGAGTCAGCAGTAGCCTCATCATCACTAGATGGCATTTCTTCTGAGCAAAACAGGT  (R1)

NAAATGCCATCTAGTGATGATGAGGCTACTGCTGACTCTCAACATTCTACTCCTCCAAAAAAGAAGAGAAAGATTCCAACCCCCAGAACCGATGACCGGCA  (R4)

R1 is not the reverse complement of R4. These files contain the paired end reads. 

| File name | label | Read length | Phred encoding |
|---|---|---|---|
| 1294_S1_L008_R1_001.fastq.gz | read1 | 101 | Phred+33 |
| 1294_S1_L008_R2_001.fastq.gz | index1 | 8 | Phred+33 |
| 1294_S1_L008_R3_001.fastq.gz | index2 | 8 | Phred+33 |
| 1294_S1_L008_R4_001.fastq.gz | read2 | 101 | Phred+33 |

This is the list of 24 indices stored in Talapas:
```/projects/bgmp/shared/2017_sequencing/indexes.txt```

sample  group   treatment       index   index sequence
1       2A      control B1      GTAGCGTA
2       2B      control A5      CGATCGAT
3       2B      control C1      GATCAAGG
4       2C      mbnl    B9      AACAGCGA
6       2D      mbnl    C9      TAGCCATG
7       2E      fox     C3      CGGTAATC
8       2F      fox     B3      CTCTGGAT
10      2G      both    C4      TACCGGAT
11      2H      both    A11     CTAGCTCA
14      3B      control C7      CACTTCAC
15      3C      mbnl    B2      GCTACTCT
16      3D      mbnl    A1      ACGATCAG
17      3E      fox     B7      TATGGCAC
19      3F      fox     A3      TGTTCCGT
21      3G      both    B4      GTCCTAAG
22      3H      both    A12     TCGACAAG
23      4A      control C10     TCTTCGAC
24      4A      control A2      ATCATGCG
27      4C      mbnl    C2      ATCGTGGT
28      4D      mbnl    A10     TCGAGAGT
29      4E      fox     B8      TCGGATTC
31      4F      fox     A7      GATCTTGC
32      4G      both    B10     AGAGTCCA
34      4H      both    A8      AGGATAGC


Determined the length of the reads in each file:

```zcat 1294_S1_L008_R1_001.fastq.gz | head -2 | tail -1 | wc -m```
This file has 101 reads (returned 102, but subtracted 1 for the newline character).

```zcat 1294_S1_L008_R2_001.fastq.gz | head -2 | tail -1 | wc -m```
This file has 8 reads (returned 9, but subtracted 1 for the newline character).

```zcat 1294_S1_L008_R3_001.fastq.gz | head -2 | tail -1 | wc -m```
This file has 8 reads (returned 9, but subtracted 1 for the newline character).

```zcat 1294_S1_L008_R4_001.fastq.gz | head -2 | tail -1 | wc -m```
This file has 101 reads (returned 102, but subtracted 1 for the newline character).

Determine the phred encoding for these data.

```zcat 1294_S1_L008_R1_001.fastq.gz | head -4 | tail -1```

A#A-<FJJJ<JJJJJJJJJJJJJJJJJFJJJJFFJJFJJJAJJJJ-AJJJJJJJFFJJJJJJFFA-7<AJJJFFAJJJJJF<F--JJJJJJF-A-F7JJJJ

The characters #, -, and < all have Phred scores less than 64, which means that this file uses Phred+33 encoding.

```zcat 1294_S1_L008_R2_001.fastq.gz | head -4 | tail -1```

#AA<FJJJ

The characters # and < both only occur in Phred+33 encoding.

```zcat 1294_S1_L008_R3_001.fastq.gz | head -4 | tail -1```

#AAAAJJF

The character # only occurs in Phred+33 encoding.

```zcat 1294_S1_L008_R4_001.fastq.gz | head -4 | tail -1```

#AAFAFJJ-----F---7-<FA-F<AFFA-JJJ77<FJFJFJJJJJJJJJJAFJFFAJJJJJJJJFJF7-AFFJJ7F7JFJJFJ7FFF--A<A7<-A-7--

The characters #, -, and < only occur in Phred+33 encoding.


After creating dictionary for list of indices, checked in terminal line to see how many files were created:

```ls -1 *.fq | wc -l```

Labeling convention:
    AAA_R1.fq
    AAA_R2.fq

Created unit tests:
```
zcat 1294_S1_L008_R1_001.fastq.gz | head -40 > /projects/bgmp/csung/bioinfo/Bi622/Demultiplexing/test_R1.fq
zcat 1294_S1_L008_R2_001.fastq.gz | head -40 > /projects/bgmp/csung/bioinfo/Bi622/Demultiplexing/test_R2.fq
zcat 1294_S1_L008_R3_001.fastq.gz | head -40 > /projects/bgmp/csung/bioinfo/Bi622/Demultiplexing/test_R3.fq
zcat 1294_S1_L008_R4_001.fastq.gz | head -40 > /projects/bgmp/csung/bioinfo/Bi622/Demultiplexing/test_R4.fq
```
