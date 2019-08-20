import argparse
import glob
import eaf_reader
import os
from tqdm import tqdm

def get_annotation_list(file_name):
	'''

	'''
	eaf_file = eaf_reader.Eaf(file_name)
	tier_name = list(eaf_file.get_tier_names())[0]
	annotations_list = ""
	
	for start_time, end_time, text in eaf_file.get_annotation_data_for_tier(tier_name):
		new_line = "{}\t{}\t{}".format(start_time, end_time, text)
		annotations_list = annotations_list + new_line + "\n"
	
	return(annotations_list)

def write_as_txt(source_dir, output_dir):
	'''
	
	'''
	if not os.path.exists(output_dir):
		os.mkdir(output_dir)

	eaf_files_list = glob.glob('{}/*.eaf'.format(source_dir))

	for eaf_file_path in tqdm(eaf_files_list):
		annotations_list = get_annotation_list(eaf_file_path)
		txt_file_path = ''.join([output_dir, eaf_file_path[len(source_dir):-4], '.txt'])
			
		with open(txt_file_path, 'w') as file:
			file.write(annotations_list)

	print("{} files converted successfully!".format(len(eaf_files_list)))

def get_args():
	'''

	'''
	parser = argparse.ArgumentParser(description='Converts .eaf to .txt')
	parser.add_argument(
		'source_dir',
		type=str,
		help='source directory'
	)
	parser.add_argument(
		'output_dir',
		type=str,
		help='output directory'
	)
	return parser.parse_args()	

def main():
	args = get_args()
	write_as_txt(args.source_dir, args.output_dir)

if __name__ == "__main__":
	main()