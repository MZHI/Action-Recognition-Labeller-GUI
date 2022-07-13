#!/bin/bash

# Run label tool file by file from directory VIDEOSPATH
# For each video created own label csv file in directory --out_csv_root
# For go to next video, just close current label program instance, and new processed videofile will be written to LOGSFILE
# All processed files from LOGSFILE will be skipped. To label all files from scratch, just remove LOGSFILE and also remove --out_csv_root

VIDEOSPATH="./videos"
LOGSFILE="processed.txt"

echo $( pwd )

IFS=$'\n'
files=($(find ${VIDEOSPATH} -type f -regex "^.*$"))
for filename in ${files[*]}
do
  echo "Video file: "${filename}

  # try to find processed file in "processed.txt" file
  echo "CHECKING processed.txt"
#  is_processed=0
  while read line;
  do
    echo $line
    if [ ${line} == ${filename} ]; then
      echo "Processed file found!!!"
      continue 2
    fi
  done < ${LOGSFILE}
  echo "Processing "${filename}
  echo "main.py --mode single --video_path \"${filename}\" --classes_csv classes_tng.csv --out_csv_root labels"
  python main.py --mode single --video_path "${filename}" --classes_csv classes_tng.csv --out_csv_root labels
#  echo ${filename} >> ${LOGSFILE} # now doing this in main.py !!!
done
IFS=

