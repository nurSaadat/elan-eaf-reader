import glob
import pympi

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
	print("time: {}:{}.{}".format(minutes, seconds, millisec)) 

def print_space_error(annotation):
	"""Prints whether there is a space before or after a string

	Parameters:
		annotation (tuple): start time, end time and content 
						of a single annotation  

	Returs:
		None

	"""
	text = annotation[2]
	if text.startswith(' '):
		print("space start {}".format(annotation))
		print_time(annotation)
		print("{:*^30}".format(''))
	if text.endswith(' '):
		print("space end {}".format(annotation))
		print_time(annotation)
		print("{:*^30}".format(''))

def print_time_error(annotation_1, annotation_2):
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
	print("gap between {} and {}". format(annotation_1, annotation_2))
	print_time(annotation_1)
	print("time gap {}".format(time_dif))
	print("{:*^30}".format(''))

def get_annotation_list(file_name):
	"""Reads .eaf file and returns a list of all annotations

	Parameters:
		file_name (str): directory of a source file  

	Returs:
		annotations_list (list): all annotations of a single document 

	"""
	eaf = pympi.Elan.Eaf(file_name)
	tier_name = list(eaf.get_tier_names())[0]
	annotations_list = eaf.get_annotation_data_for_tier(tier_name)
	return(annotations_list)

def main():
	data_dir = '/home/saadat/akbilek'
	for file_path in glob.glob('{}/*.eaf'.format(data_dir)):
		annot_list = get_annotation_list(file_path)
		print("looking in {} ...".format(file_path))
		for i in range(len(annot_list) - 1):
			print_space_error(annot_list[i])
			if annot_list[i][1] != annot_list[i + 1][0]:
				print_time_error(annot_list[i], annot_list[i + 1])
		print_space_error(annot_list[-1])

if __name__ == "__main__":
	main()