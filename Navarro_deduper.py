#!/usr/bin/env python

import argparse
import re

#ARGPARSE
def get_args():
    parser = argparse.ArgumentParser(description="This function need a sorted sam input file and known UMI text file. It will output a deduped sam file.")
    parser.add_argument("-f", "--input", required=True, type=str, help="absolute filepath to sorted .sam file")
    parser.add_argument("-o", "--output", required=False, type=str, help="absolute filepath to output sam file")
    parser.add_argument("-u", "--umi", required=True, type=str, help="absolute filepath to list of UMIs")
    return(parser.parse_args())

args = get_args()
input_file = args.input
output_file = args.output
UMI_file = args.umi

#FUNCTIONS
def get_UMI(qname):
    '''Gets UMI from a qname.'''
    split_qname=qname.split(":")
    UMI=split_qname[-1]
    return UMI
  
def check_flag(flag):
    '''Determines whether the read is from forward or reverse strand using the bitwise flag.''' 
    if (flag & 16)!=16:
        return "forward"
    elif (flag & 16)==16:
        return "reverse"

def adjust_position(cigar, position, strand):
    '''Gets the left most start position from SAM file using cigar string, position, and strand ID. 
    Adjusts as needed for soft clipping. This will adjust differently depending if it is a forward or reverse read.'''
    cigar_list=[] 
    cigar_list=re.findall(r'([0-9]+)([MNDS])',cigar) 
    #will add to list as tuple in format [(number,letter)]
    if strand == "reverse":
        if cigar_list[0][1] == "S": #if S is the first position we don't want to take it into account
            cigar_list.pop(0) #removes any S on the left hand side so we only soft clip for right hand side 
            for i in range(len(cigar_list)): #iterates through list
                position+=int(cigar_list[i][0]) #adds number to position 
        else: #if there is no S we don't need to remove 
            for i in range(len(cigar_list)): #iterates through list
                position+=int(cigar_list[i][0]) #adds number to position 
        return position #returns the adjusted position 
    if strand == "forward":
        if cigar_list[0][1] == "S": #we only want to take into account the left hand S
            position=position-int(cigar_list[0][0]) #subtract from position 
        return position #return adjusted position 

#CREATING UMI SET
with open(UMI_file,"r") as fh1: #creating a known UMIs set 
    UMI_set=set()
    for line in fh1: 
        line=line.strip("\n")
        UMI_set.add(line)

#MAIN FUNCTION
with open(input_file, "r") as input, open(output_file,"w") as output:

    #counters: 
    unique=0
    duplicates=0
    unknown_UMIs=0
    unique_dict={} 
    #keys are the things we want (UMI,flag,adjusted_position,chromosome), values are just a placeholder number
    prev_chrom=""
    chrom_dict={} #to be used to count the different unique chromsome numbers

    for line in input:
        line=line.strip("\n")
        if line.startswith("@"): #If there is a header line write it to the output file 
            print(f"{line}",file=output)
        else: 
            line_info=line.split("\t")
            #grab the info we need from the line 
            chrom=line_info[2]
            flag=line_info[1]
            strand=check_flag(int(flag))
            position=int(line_info[3])
            cigar=line_info[5]
            adjusted_position=adjust_position(cigar,position,strand)
            UMI=get_UMI(line_info[0])
            if UMI in UMI_set:#check to see if UMI is known 
                if prev_chrom == chrom:
                    if (UMI,flag,adjusted_position,chrom) in unique_dict.keys():
                        duplicates+=1  
                    else:
                        print(f"{line}",file=output)
                        unique_dict[(UMI,flag,adjusted_position,chrom)]=1
                        unique+=1 #add to unique counter
                        chrom_dict[chrom]+=1
                elif  prev_chrom != chrom: #comparing to see if the chromosomes are the same
                    prev_chrom=chrom #if they are not make the prev one equal to the current number
                    unique_dict.clear() #and empty dictionary to save memory 
                    print(f"{line}",file=output)
                    unique_dict[(UMI,flag,adjusted_position,chrom)]=1 #add to dictionary since new chrom means unique read 
                    unique+=1 #add to unique counter
                    chrom_dict[chrom]=1 #add the chrom number to chrom dictionary 
            else:
                unknown_UMIs+=1 #add to unknown counter

#Writing to report file now
with open("report2.txt", "w") as fh1:
    print(f"Number unique reads:{unique}",file=fh1)
    print(f"Number duplicate reads:{duplicates}", file=fh1)
    print(f"Number unknown UMIS:{unknown_UMIs}", file=fh1)
    for key,value in chrom_dict.items():
        print(f"Number of chromosome {key}: {value}", file=fh1)

        



    
