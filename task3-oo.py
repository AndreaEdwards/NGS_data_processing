"""
Task:
Given a chromosome and coordinates, write a program for looking up its 
annotation.  Keep in mind you'll be doing this annotation millions of times.
	-	Input: 
		o	Tab-delimited file: Chr<tab>Position
		o	GTF formatted file with genome annotations.
	-	Output: 
		o	Annotated file of gene name that input position overlaps.
	-	Hint: Most of the sequence reads come from a small portion of 
	the genome. Try to use this information to improve performance, 
	if possible.

Example usage:
python task3-oo.py

Results are written to output.txt
"""

from task_objects import (FileHandlers, Task3Handlers)


def main():
	#instantiate objects
	file_handlers = FileHandlers()
	task3 = Task3Handlers()

	#locate files
	file_paths = file_handlers.search_directory()
	txt_files = file_handlers.find_files(file_paths, 'txt')
	files_to_annotate = file_handlers.filter_files(txt_files, '\t')
	annotations = file_handlers.find_files(file_paths, 'gtf')

	#calculate and write results to output.txt
	for item in annotations:
		chr_dict = task3.map_chr_dicts(item)
		red_chr_dict = task3.reduce_chr_dicts(chr_dict)
	for item in files_to_annotate:
		task3.search_coordinates(red_chr_dict, item)

main()