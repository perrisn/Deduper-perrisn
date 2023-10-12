# Deduper Pseudocode
##Problem

This program will aim to remove all PCR duplicates from a sorted sam file. A PCR duplicate is any two reads that came from the same cDNA fragment. Removing them before moving to downstream analyses can help reduce bias and reduce false positive variant calls. We will use Unique Molecular Indexes (UMI) to remove duplicates. A PCR duplicate will have the following: 
+They have the same UMI
+They are on the same chromosome (flag 3)
+They are on the same strand (flag 2)
+They start at same 5' position (flag 4)

We need to keep in mind that there could be soft clipping as well. Soft clipping refers to an end of the sequence that did not align well to the genome. We can utilize the CIGAR string in order to determine whether soft clipping has occured or not. 

A few things we need to keep in mind: 
+There are millions of reads, so we should try to avoid loading everything into memory. 
+Make sure we are utilizing functions. 
+Have commented code and include doc strings! 

##Functions:
```
def check_UMI:
'''Determines whether an UMI in a given file is in a list of given UMIs or not. If it is, returns TRUE. If not, returns FALSE.'''
Extracts UMI from QNAME 
Compares against known dictionary
Return whether it passes or not 
Example input: NS500451:154:HWKTMBGXX:1:11101:15364:1139:GAACAGGT
Example return: TRUE 
```
```
def soft_clip:
'''Determines whether a read has been soft clipped or not by searching for S in the CIGAR string. Also looks to see whether the read is forward v. reverse mapped. If it has, adjusts the start position for the soft clipping. Reads that have not been soft clipped will return the original starting position.'''
Get CIGAR string and determine whether there has been soft clipping (soft clipping would be denoted by an S) 
Uses bitwise flag to see if it is forward or reverse read. 
Adjust start position for soft clipping (or skip if not soft clipped).
Return adjusted position
Example input: read1	0	2	200	36	2S5M	*	0	0	TCCACCA	<EEEEEE	MD:Z:71	
Example return: 198
```
##Main body: 
+Store the known UMIs in a dictionary with UMIs as keys and alignment position as values 
+Implement argparse to be able to enter files of interest on command line. 
+Use samtools to sort the file based on the chromosome and position (if needed). 
+Iterate through each read in the file.Write lines with @ as these are header lines to the final output file but otherwise ignore them.
+Store current read in list (split on tabs). Define the info you need from each read (UMI, chromosome, position, CIGAR, strand). 
+Check to see if read is mappeed or unmapped by looking at the bitwise flag. 
+See if UMI found in QNAME is in dictionary of known UMIS using function (check_UMI).
	+If it does not match a known UMI skip read. Write to a file that will retain all unknown UMIs due to sequencing errors. 
	+If it does match:
		+Add UMI as key in dictionary with value as chromosome, position, and strand.  
		+Write to output file. 
+Use CIGAR string to check if the read is soft-clipped or not using function (soft_clip). 
	+If it is soft clipped, the function will adjust the position.
+Check if the position, strand, etc is already in the dictionary by comparing the keys and values. 
+"Retain" read if it is different than any values in dictionary so far. Write this to an output file.  
+If it is the same as other in dictionary, write to a separate file to track duplicated reads that were removed.
+Once the chromosome changes, empty the dictionary.  


##Expected output files: 
+One file with reads we are keeping that have been DEDUPED! 
+One file with removed duplicates
+One file with UMIs that were unknown (potentially due to sequencing errors) 