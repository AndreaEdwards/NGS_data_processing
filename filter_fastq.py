"""
Recursively find all FASTQ files in a directory and report each file 
name and the percent of sequences in that file that are greater than 
30 nucleotides long.

Example usage:
python task1-oo.py

Results are output on CLI
"""

from task_objects import (FileHandlers, PrettyPrint, Task1Handlers)


def main():
	#instantiate objects
	file_handlers = FileHandlers()
	pretty_print = PrettyPrint()
	task1 = Task1Handlers()
	
	#locate files
	file_paths = file_handlers.search_directory()
	fastq_files = file_handlers.find_files(file_paths, 'fastq')
	
	#filter by sequence length (seqs will include Ns)
	filter_length = int(input("What length do you want to set as your cutoff? "))
	
	#print header
	pretty_print.prepare_format1('fastq file path', 'percent of seqs with length >', filter_length)
	pretty_print.print_stars(fastq_files)
	
	#calculate and print results to CLI
	for file_name in fastq_files:
		fastq_dict = task1.parse_fastq(file_name)
		filtered_dict = task1.filter_by_length(fastq_dict, filter_length)
		percent = (float(len(filtered_dict))/len(fastq_dict)) * 100
		print file_name.ljust(0), str('%.2f' % percent + '%').rjust(100-(len(file_name)))


main()