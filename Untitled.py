import my_elan

def write_as_txt(eaf_file_name):
	eaf_file = my_elan.Eaf(eaf_file_name)

	tier_name = list(eaf_file.get_tier_names())[0]
	annotations_list = ""
	for annotation in example_eaf.get_annotation_data_for_tier(tier_name):
		start_time, end_time, text = annotation
		new_line = "{}\t{}\t{}".format(start_time, end_time, text)
		annotations_list = annotations_list + new_line + "\n"

	file_path = ''.join([eaf_file_name[:-4], '.txt'])
	with open(file_path, 'w') as file:
		file.write(annotations_list)


def main():
	for file_path in glob.glob('{}/*.eaf'.format(data_directory)):


if __name__ == "__main__":
	main()
