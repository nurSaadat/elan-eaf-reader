import argparse
import datetime 
import os
import my_elan
from tqdm import tqdm

def write_as_txt(eaf_file_name):
	eaf_file = my_elan.Eaf(eaf_file_name)
	tier_name = list(eaf_file.get_tier_names())[0]
	annotations_list = ""
	for annotation in tqdm(eaf_file.get_annotation_data_for_tier(tier_name)):
		start_time, end_time, text = annotation
		new_line = "{}\t{}\t{}".format(start_time, end_time, text)
		annotations_list = annotations_list + new_line + "\n"

	file_path = ''.join([eaf_file_name[:-4], '.txt'])

	with open(file_path, 'w') as file:
		file.write(annotations_list)

def log_time(milliseconds):
	"""Prints the exact time of annotation

	Parameters:
		annotation (tuple): start time, end time and content 
						of a single annotation  

	Returs:
		None

	"""
	seconds = milliseconds * 0.001
	minutes = int(seconds // 60)
	seconds = int(seconds % 60)
	millisec = int(milliseconds % 1000)

def remove_space_error(annotation_text):
	"""Checks whether there is a space before or after a string

	Parameters:
		annotation (tuple): start time, end time and content 
						of a single annotation  

	Returs:
		None

	"""
	if annotation_text.startswith(' '):
		annotation_text = annotation_text[1:]
	if annotation_text.endswith(' '):
		annotation_text = annotation_text[:-1]
	return annotation_text

def remove_time_error(end_time_1, start_time_2):
	"""Prints whether there is a time gap between two annotations

	Parameters:
		annotation_1 (tuple): start time, end time and content 
						of a single annotation before the gap
		annotation_2 (tuple): start time, end time and content 
						of a single annotation after the gap

	Returs:
		None

	"""
	time_dif = start_time_2 - end_time_1
	if time_dif < 20:
		return end_time_1
	else:
		return start_time_2
	
def clean_eaf(src_file):
	old_eaf = my_elan.Eaf(src_file)
	media_descriptors = old_eaf.media_descriptors
	properties = old_eaf.properties
	tier_name = list(old_eaf.get_tier_names())[0]

	new_eaf = my_elan.Eaf()
	new_eaf.media_descriptors = media_descriptors
	new_eaf.properties = properties

	prev_end_time = None
	for annotation in tqdm(old_eaf.get_annotation_data_for_tier(tier_name)):
		start_time, end_time, text = annotation
		if prev_end_time:
			start_time = remove_time_error(prev_end_time, start_time)
		text = remove_space_error(text)
		new_eaf.add_annotation(tier_name, start_time, end_time, value=text)
		prev_end_time = end_time
	new_eaf.to_file(src_file)    

def get_args():
	parser = argparse.ArgumentParser(description='Edit and work with .eaf files')
	parser.add_argument(
		'mode',
		type=str,
		help='eaf_to_txt or clean_eaf'
	)
	parser.add_argument(
		'src_file',
		type=str,
		help='source file'
	)	
	return parser.parse_args()	

def main():
	args = get_args()
	data_directory = 'data/'
	if not os.path.exists(data_directory):
		os.mkdir(data_directory)
	args.src_file = "".join([data_directory, args.src_file])

	if args.mode == 'eaf_to_txt':
		write_as_txt(args.src_file)
	elif args.mode == 'clean_eaf':
		clean_eaf(args.src_file)	

if __name__ == "__main__":
	main()