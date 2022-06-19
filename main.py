from tkinter import *
from label_gui import label_GUI
from pathlib import Path
import argparse
import os


def arg_parse():
	parser = argparse.ArgumentParser(description='Arguments for the GUI action recognition video labeler')
	parser.add_argument("--mode", dest="mode", help='Can be either "single" label mode or noun-verb "duo" mode')
	parser.add_argument("--video_path", dest="video_path", help="Path to video being labelled, or dir with videos")
	parser.add_argument("--label_csv", dest="label_csv", help="Path to csv file where labels will be stored")
	parser.add_argument("--classes_csv", dest="classes_csv", help="Path to csv file containing all labels")
	parser.add_argument("--verb_csv", dest="verb_csv", help="Path to csv file containing all verb labels")
	parser.add_argument("--noun_csv", dest="noun_csv", help="Path to csv file containing all noun labels")
	parser.add_argument("--out_csv_root", dest="out_csv_root", help="Root path to output csv files")

	return parser.parse_args()


def on_closing(root):
	# save name of label file into log file
	global video_name
	mode_write = "w" if not Path("processed.txt").is_file() else "a"
	with open("processed.txt", mode_write) as fh:
		fh.write(video_name + "\n")
	root.destroy()


if __name__ == '__main__':	
	
	root = Tk()
	args = arg_parse()

	mode = args.mode
	video_path = args.video_path
	video_name = Path(video_path).name
	label_csv = args.label_csv
	out_csv_root = args.out_csv_root

	# is_batch_process = False
	# if not Path(video_path).is_file():
	# 	is_batch_process = True


	modes = ['single','duo']
	if mode not in modes:
		print('Error, mode {} not recognised, please enter either single or duo mode'.format(mode))
		quit()

	if args.mode == 'duo':  #if using verb,noun labeling system.
		verb_csv = args.verb_csv
		noun_csv = args.noun_csv
		classes_csv = verb_csv, noun_csv

	classes_csv = None
	if args.mode == 'single':
		classes_csv = args.classes_csv

	# check for existence of csv output file, if no, then create
	csv_path = label_csv
	if label_csv is None:
		csv_path = Path(video_path).stem + ".csv"
	if out_csv_root is not None:
		if not Path(out_csv_root).is_dir():
			Path(out_csv_root).mkdir(exist_ok=True, parents=True)
		csv_path = os.path.join(out_csv_root, csv_path)
	if not Path(csv_path).is_file():
		with open(csv_path, "w") as f:
			f.write("Vid_id,start_frame,end_frame,class,class_id\n")

	root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))

	label_GUI(root, video_path, csv_path, classes_csv, mode)
