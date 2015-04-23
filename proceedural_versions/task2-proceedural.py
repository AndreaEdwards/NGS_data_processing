"""
Given a FASTA file with DNA sequences, find 10 most frequent sequences 
and return the sequence and their counts in the file.
"""

import os

def search_directory():
	working_directory = os.getcwd()
	file_paths = []
	for root, directory, file_list in os.walk(working_directory):
		for file_name in file_list:
			path = root + os.sep + file_name
			file_paths.append(path)
	return file_paths

def find_fasta(file_list):
	fastq_file_list = []
	for file_path in file_list:
		new_list = file_path.split('.')
		if new_list[1] == 'fasta':
			fastq_file_list.append(file_path)
		else:
			pass
	return fastq_file_list


def count_seqs(fasta_file):
	fasta_dict = {}
	for line in open(fasta_file):
		if line.startswith('>'):
			pass
		elif line in fasta_dict:
			fasta_dict[line] += 1
		else:
			fasta_dict[line] = 1 
	return fasta_dict

def get_top_seqs(fasta_dict, threshold):
	sorted_list = []
	for seq in sorted(fasta_dict, key=fasta_dict.get, reverse=True):
		sorted_list.append([seq.strip('\n'), fasta_dict[seq]])
	return sorted_list[:threshold] #does not account for multiple seqs with same count


def print_stars(list):
	name_length_list = [len(name) for name in list]
	stars = ''
	for number in range(max(name_length_list)):
		stars += '*'
	for number in range(0, (100-(max(name_length_list))+1)):
		stars += '*'
	print(stars)


def main():
	file_paths = search_directory()
	fasta_files = find_fasta(file_paths)
	threshold = raw_input("Enter an integer value for the number of most" +
							 "frequently observed sequences you would like" +
							 "displayed (default is top 10) ")
	if threshold == '':
		threshold = 10
	else:
		threshold = int(threshold)
	for file_name in fasta_files:
		fasta_dict = count_seqs(file_name)
		top_seqs = get_top_seqs(fasta_dict, threshold)
		print "\n"
		print "The top ", threshold, "sequences observed are: "
		print "\n"
		print "sequence".ljust(0), "counts".rjust(100-len("sequence"))
		print_stars(top_seqs)
		for list_item in top_seqs:
			print str(list_item[0]).ljust(0), str(list_item[1]).rjust(100 - len(list_item[0]))


main()