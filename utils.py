#some utility classes and functions for the GUI, mainly video processing.
import os
from PIL import Image 
from pathlib import Path


def decode_video(video_path):
	"""
	function that decodes a given video into its frames and stores them in a folder of the same named "/data/videoname"
	returns the name of the video and the new_folder path for use in main.py
	"""

	# if running first time must create data folder.
	if os.path.exists('data') == False:
		os.mkdir('data')	

	# check if decoding has been done before, if so use that file
	# video_name = os.path.basename(video_path)[:-4]
	video_name = Path(video_path).stem

	new_folder = os.path.join('data', video_name)

	bash_cmd = 'ffmpeg -i \"{}\" -vf scale=-1:720 -q:v 0 {}/%06d.jpg'.format(
		video_path,
		new_folder)  # create clips.
	if os.path.isdir(new_folder):  # if folder already exists
		if len(os.listdir(new_folder)) == 0:  # if folder is empty, decode the video into it.
			print('decoding the video, this may take a while... Once finished GUI will load')
			# print(video_path)
			# print(bashCommand)
			os.system(bash_cmd)
			return new_folder

		else:
			print('A folder with this video name already exists, loading that instead (much quicker)')
			return new_folder

	else:  # need to decode the video into a folder of images - makes life easier...
		print('decoding the video, this may take a while... Once finished GUI will load')
		os.mkdir(new_folder)
		os.system(bash_cmd)

		return new_folder


def get_image(folder, idx):
	"""
	given a folder of images and an id will return a PIL image of that index (this assumes images are stored with names in alpabetical order - this should be true unless you renamed images )
	"""
	image_name = sorted(os.listdir(folder))[idx]
	image_path = os.path.join(folder, image_name)
	
	return Image.open(image_path)
