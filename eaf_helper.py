import argparse
import datetime 
import glob
import logging
import os
import my_elan

def write_as_txt(eaf_file_name):
	eaf_file = my_elan.Eaf(eaf_file_name)
	tier_name = list(eaf_file.get_tier_names())[0]
	annotations_list = ""
	for annotation in eaf_file.get_annotation_data_for_tier(tier_name):
		start_time, end_time, text = annotation
		new_line = "{}\t{}\t{}".format(start_time, end_time, text)
		annotations_list = annotations_list + new_line + "\n"

	file_path = ''.join([eaf_file_name[:-4], '.txt'])

	with open(file_path, 'w') as file:
		file.write(annotations_list)

def print_time(annotation):
	"""Prints the exact time of annotation

	Parameters:
		annotation (tuple): start time, end time and content 
						of a single annotation  

	Returs:
		None

	"""
	seconds = annotation[1] * 0.001
	minutes = int(seconds // 60)
	seconds = int(seconds % 60)
	millisec = int(annotation[1] % 1000)
	logging.info("time: {}:{}.{}".format(minutes, seconds, millisec)) 

def space_error(annotation):
	"""Checks whether there is a space before or after a string

	Parameters:
		annotation (tuple): start time, end time and content 
						of a single annotation  

	Returs:
		None

	"""
	text = annotation[2]
	if text.startswith(' '):
		logging.info("space start {}".format(annotation))
		print_time(annotation)
		logging.info("{:*^30}".format(''))
	if text.endswith(' '):
		logging.info("space end {}".format(annotation))
		print_time(annotation)
		logging.info("{:*^30}".format(''))

def time_error(annotation_1, annotation_2):
	"""Prints whether there is a time gap between two annotations

	Parameters:
		annotation_1 (tuple): start time, end time and content 
						of a single annotation before the gap
		annotation_2 (tuple): start time, end time and content 
						of a single annotation after the gap

	Returs:
		None

	"""
	time_dif = annotation_2[0] - annotation_1[1]
	logging.info("gap between {} and {}". format(annotation_1, annotation_2))
	print_time(annotation_1)
	logging.info("time gap {}".format(time_dif))
	logging.info("{:*^30}".format(''))

def get_annotation_list(file_name):
	"""Reads .eaf file and returns a list of all annotations

	Parameters:
		file_name (str): directory of a source file  

	Returs:
		annotations_list (list): all annotations of a single document 

	"""
	eaf = my_elan.Eaf(file_name)
	tier_name = list(eaf.get_tier_names())[0]
	annotations_list = eaf.get_annotation_data_for_tier(tier_name)
	return(annotations_list)

def clean_eaf(data_directory):
	if not os.path.exists(data_directory):
		os.mkdir(data_directory)

	for file_path in glob.glob('{}/*.eaf'.format(data_directory)):
		annot_list = get_annotation_list(file_path)
		logging.info("Currently in {} .".format(file_path))
		logging.info("{:=^30}".format(''))
		for i in range(len(annot_list) - 1):
			space_error(annot_list[i])
			if annot_list[i][1] != annot_list[i + 1][0]:
				time_error(annot_list[i], annot_list[i + 1])
		space_error(annot_list[-1])

def get_args():
	parser = argparse.ArgumentParser(description='Edit and work with .eaf files')
	parser.add_argument(
		'src_file',
		type=str,
		help='source file'
	)
	parser.add_argument(
		'mode',
		type=str,
		help='eaf_to_txt or clean_eaf'
	)
	return parser.parse_args()	

def init_logger():
	file_name = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	log_directory = "log/"
	if not os.path.exists(log_directory):
		os.mkdir(log_directory)
	log_path = "".join([log_directory, file_name, '.log'])
	logging.basicConfig(
		filename=log_path, 
		level=logging.INFO,
		format='%(message)s\n'
	)

def main():
	init_logger()
	args = get_args()
	if args.mode == 'eaf_to_txt':
		write_as_txt(args.src_file)
	# elif args.mode == 'clean_eaf':
	# 	clean_eaf(args.src_file)	

if __name__ == "__main__":
	main()