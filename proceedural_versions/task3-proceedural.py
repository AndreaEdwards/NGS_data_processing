"""
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


def find_files(file_list, extension):
	new_file_list = []
	for file_path in file_list:
		new_list = file_path.split('.')
		if new_list[1] == extension:
			new_file_list.append(file_path)
		else:
			pass
	return new_file_list


def filter_files(file_list, character):
	filtered_list = []
	for file in file_list:
		for line in open(file):
			if '\t' not in line:
				break
			else:
				filtered_list.append(file)
				break
	return filtered_list


def clean(lines):
	cleaned = []
	for field in lines:
		cleaned.append(field.strip())
	return(cleaned)


def map_chr_dicts(gtf_file):
	chr_dict = {}
	for line in open(gtf_file):
		fields = line.split()
		cleaned = clean(fields)
		chr_id, coord1, coord2, gene_name = cleaned[0], int(cleaned[3]), int(cleaned[4]), cleaned[9]
		if chr_id in chr_dict:
			if gene_name in chr_dict[chr_id]:
				chr_dict[chr_id][gene_name].append(coord1)
				chr_dict[chr_id][gene_name].append(coord2)
			else:
				chr_dict[chr_id][gene_name] = [coord1, coord2]	
		else:
			chr_dict[chr_id] = {}
			if gene_name in chr_dict[chr_id]:
				chr_dict[chr_id][gene_name].append(coord1)
				chr_dict[chr_id][gene_name].append(coord2)
			else: 
				chr_dict[chr_id][gene_name] = [coord1, coord2]
	return chr_dict


def reduce_chr_dicts(chr_dict):
	for chr_id in chr_dict:
		for gene_name in chr_dict[chr_id]:
			lower_bound = min(chr_dict[chr_id][gene_name])
			upper_bound = max(chr_dict[chr_id][gene_name])
			chr_dict[chr_id][gene_name] = [lower_bound, upper_bound]
	return chr_dict


def search_coordinates(chr_dict, coord_file):
	output_file = os.getcwd() + os.sep + 'output.txt'
	output = open(output_file, "w")

	for line in open(coord_file):
		fields = line.split()
		cleaned = clean(fields)
		chromosome, coordinate = cleaned[0], int(cleaned[1])
		if chromosome in chr_dict:
			for gene_name in chr_dict[chromosome]:
				if chr_dict[chromosome][gene_name][0] <= coordinate <= chr_dict[chromosome][gene_name][1]:
					found_coordinate = gene_name
					new_line = [chromosome, str(coordinate), gene_name.replace('"','').strip(';'), '\n']
					output.write("\t".join(new_line))
				else:
					pass
		else:
			pass
	output.close()


def main():
	file_paths = search_directory()
	txt_files = find_files(file_paths, 'txt') 
	files_to_annotate = filter_files(txt_files, '\t')
	annotations = find_files(file_paths, 'gtf')
	for item in annotations:
		chr_dict = map_chr_dicts(item)
		chr_dict = reduce_chr_dicts(chr_dict)
	for item in files_to_annotate:
		search_coordinates(chr_dict, item)


main()



