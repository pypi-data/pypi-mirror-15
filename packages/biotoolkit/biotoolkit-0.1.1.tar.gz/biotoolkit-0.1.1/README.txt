biotoolkit contains:

	GCfromDNA.py
	
	
GCfromDNA is a python module/command line utility for determining the GC content of DNA 
sequences, as read from standard fasta (.fa) files. 
This module formats each sequence name (replacing spaces with underscores), calculates the 
percentage GC-content for each sequence, and saves this data as a csv file with a modified
version of the original filename (e.g., fasta_file_1.fa --> fasta_file_1_GC.csv). 

GCfromDNA utilizes parts of the biopython package for analysis. The package 
can be installed with the following command: 

	$ pip install biopython

To install biotoolkit:
	
	$ pip install biotoolkit

Upon successful installation, the module can be imported into new python scripts with:
	
	from biotoolkit import GCfromDNA

For instance, the following is a complete python script that will invoke the module's functionality:

	#!/usr/bin/env python
	from biotoolkit import GCfromDNA
	GCfromDNA.compute()

It is possible to pass fasta filenames as parameters directly to the compute function. 
Filenames must be passed to the compute function as a list: 

	GCfromDNA.compute( [file1,file2,file3] )	#if file1 == 'file1.fa', for instance

GCfromDNA can be utilized interactively. From the command line, enter:
	
	$ python
	>>> from biotoolkit import GCfromDNA
	>>> GCfromDNA.compute()

The script can be invoked directly from the directory where it resides. 
Optional filename arguments must be separated by spaces:
	
	$ python GCfromDNA.py file1.fa file2.fa file3.fa
	
		or alternatively:
	
	$ python GCfromDNA.py *.fa

If no filename is provided, the program prompts the user to select from fasta files (located 
in the current directory) for processing. 

