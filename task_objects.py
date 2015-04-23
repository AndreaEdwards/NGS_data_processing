import os


class FileHandlers:
	def __init__(self):
		self.directory = os.getcwd()
		self.file_paths = []
		self.new_file_list = []
		self.cleaned = []
		self.filtered_list = []


	def search_directory(self):
		for root, self.directory, file_list in os.walk(self.directory):
			for file_name in file_list:
				path = root + os.sep + file_name
				self.file_paths.append(path)
		return self.file_paths


	def find_files(self, file_list, extension):
		self.new_file_list = []
		for file_path in file_list:
			new_list = file_path.split('.')
			if new_list[1] == extension:
				self.new_file_list.append(file_path)
			else:
				pass
		return self.new_file_list


	def filter_files(self, file_list, character):
		for file in file_list:
			for line in open(file):
				if '\t' not in line:
					break
				else:
					self.filtered_list.append(file)
					break
		return self.filtered_list


	def clean(self, lines):
		#cleaned = []
		for field in lines:
			self.cleaned.append(field.strip()) 
		return(self.cleaned)


class PrettyPrint:
	def __init__(self):
		self.stars = ''

	def print_stars(self, file_list):
		name_length_list = [len(name) for name in file_list]
		for number in range(max(name_length_list)):
			self.stars += '*'
		for number in range(0, (100-(max(name_length_list))+1)):
			self.stars += '*'
		print(self.stars)

	def prepare_format1(self, message1, message2, number):
		print "\n"
		print message1.ljust(0), str(message2 + str(number)).rjust(100-len(message1))

	def prepare_format2(self, message1, column1, column2):
		print "\n"
		print message1
		print "\n"
		print column1.ljust(0), column2.rjust(100-len(column1))


class Task1Handlers:
	def __init__(self):
		self.fastq_dict = {}
		self.filtered_dict = {}

	def parse_fastq(self, file_name):
		file = open(file_name)
		file_content = file.readlines()
		i = 0
		while i < len(file_content):
			if i % 4 == 0:
				self.fastq_dict[file_content[i].strip('\n')] = file_content[i+1].strip('\n')
				i += 1
			else:
				i += 1
		return self.fastq_dict


	def filter_by_length(self, fastq_dict, filter_length):
		for key in fastq_dict:
			if len(fastq_dict[key]) >= filter_length:
				self.filtered_dict[key] = fastq_dict[key]
		return self.filtered_dict 


class Task2Handlers:
	def __init__(self):
		self.fasta_dict = {}
		self.sorted_list = []

	def request_threshold(self):
		threshold = raw_input("Enter an integer value for the number of most" +
							 "frequently observed sequences you would like" +
							 "displayed (default is top 10) ")
		if threshold == '':
			threshold = 10
		else:
			threshold = int(threshold)
		return threshold

	def count_seqs(self, fasta_file):
		for line in open(fasta_file):
			if line.startswith('>'):
				pass
			elif line in self.fasta_dict:
				self.fasta_dict[line] += 1
			else:
				self.fasta_dict[line] = 1 
		return self.fasta_dict

	def get_top_seqs(self, fasta_dict, threshold):
		for seq in sorted(fasta_dict, key=fasta_dict.get, reverse=True):
			self.sorted_list.append([seq.strip('\n'), fasta_dict[seq]])
		return self.sorted_list[:threshold] #does not account for multiple seqs with same count


class Task3Handlers:
	def __init__(self):
		self.chr_dict = {}

	def map_chr_dicts(self, gtf_file):
		for line in open(gtf_file):
			fields = line.split()
			file_handlers = FileHandlers()
			cleaned = file_handlers.clean(fields)
			chr_id, coord1, coord2, gene_name = cleaned[0], int(cleaned[3]), int(cleaned[4]), cleaned[9]
			if chr_id in self.chr_dict:
				if gene_name in self.chr_dict[chr_id]:
					self.chr_dict[chr_id][gene_name].append(coord1)
					self.chr_dict[chr_id][gene_name].append(coord2)
				else:
					self.chr_dict[chr_id][gene_name] = [coord1, coord2]	
			else:
				self.chr_dict[chr_id] = {}
				if gene_name in self.chr_dict[chr_id]:
					self.chr_dict[chr_id][gene_name].append(coord1)
					self.chr_dict[chr_id][gene_name].append(coord2)
				else: 
					self.chr_dict[chr_id][gene_name] = [coord1, coord2]
		return self.chr_dict


	def reduce_chr_dicts(self, chr_dict):
		for chr_id in chr_dict:
			for gene_name in chr_dict[chr_id]:
				lower_bound = min(chr_dict[chr_id][gene_name])
				upper_bound = max(chr_dict[chr_id][gene_name])
				chr_dict[chr_id][gene_name] = [lower_bound, upper_bound]
		return chr_dict


	def search_coordinates(self, chr_dict, coord_file):
		output_file = os.getcwd() + os.sep + 'output.txt'
		output = open(output_file, "w")
		for line in open(coord_file):
			fields = line.split()
			file_handlers = FileHandlers()
			cleaned = file_handlers.clean(fields)
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




