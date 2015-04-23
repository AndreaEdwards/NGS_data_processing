"""
Given a FASTA file with DNA sequences, find 10 most frequent sequences 
and return the sequence and their counts in the file.

Example usage:
python task2-oo.py

Results are output on CLI
"""

from task_objects import (FileHandlers, PrettyPrint, Task2Handlers)

def main():
	#instantiate objects
	file_handlers = FileHandlers()
	pretty_print = PrettyPrint()
	task2 = Task2Handlers()

	#locate files
	file_paths = file_handlers.search_directory()
	fasta_files = file_handlers.find_files(file_paths, 'fasta')

	#request input from user (handles int values)
	threshold = task2.request_threshold()

	for file_name in fasta_files:
		#establish data structures
		fasta_dict = task2.count_seqs(file_name)
		top_seqs = task2.get_top_seqs(fasta_dict, threshold)
		
		#print header
		message1 = "The top ", threshold, "sequences observed are: "
		pretty_print.prepare_format2(message1, 'sequence', 'counts')
		pretty_print.print_stars(top_seqs)
		
		#calculate and print results to CLI
		for list_item in top_seqs:
			print str(list_item[0]).ljust(0), str(list_item[1]).rjust(100 - len(list_item[0]))

main()