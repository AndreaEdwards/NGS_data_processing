"""
Recursively find all FASTQ files in a directory and report each file 
name and the percent of sequences in that file that are greater than 
30 nucleotides long.
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

def find_fastq(file_list):
	fastq_file_list = []
	for file_path in file_list:
		new_list = file_path.split('.')
		if new_list[1] == 'fastq':
			fastq_file_list.append(file_path)
		else:
			pass
	return fastq_file_list


def clean(lines):
	cleaned = []
	for field in lines:
		cleaned.append(field.strip())  # strip() takes out anything that is white space
	return(cleaned)


def parse_fastq(file_name):
	fastq_dict = {}
	file = open(file_name)
	file_content = file.readlines()
	i = 0
	while i < len(file_content):
		if i % 4 == 0:
			fastq_dict[file_content[i].strip('\n')] = file_content[i+1].strip('\n')
			i += 1
		else:
			i += 1
	return fastq_dict


def filter_by_length(fastq_dict, filter_length):
	filtered_dict = {}
	for key in fastq_dict:
		if len(fastq_dict[key]) >= filter_length:
			filtered_dict[key] = fastq_dict[key]
	return filtered_dict 


def print_stars(file_list):
	name_length_list = [len(name) for name in file_list]
	stars = ''
	for number in range(max(name_length_list)):
		stars += '*'
	for number in range(0, (100-(max(name_length_list))+1)):
		stars += '*'
	print(stars)


def main():
	file_paths = search_directory()
	fastq_files = find_fastq(file_paths)
	filter_length = int(input("What length do you want to set as your cutoff? "))
	print "\n"
	print 'fastq file path'.ljust(0), str('percent of seqs with length >' + str(filter_length)).rjust(100-len('fastq file path'))
	print_stars(fastq_files)
	for file_name in fastq_files:
		fastq_dict = parse_fastq(file_name)
		filtered_dict = filter_by_length(fastq_dict, filter_length)
		percent = (float(len(filtered_dict))/len(fastq_dict)) * 100
		print file_name.ljust(0), str('%.2f' % percent + '%').rjust(100-(len(file_name)))

main()