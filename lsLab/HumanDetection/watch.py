#!/usr/bin/env python
#Reference: Option1, https://askubuntu.com/questions/518457/autostart-program-whenever-a-file-is-added-to-a-folder

import subprocess
import time


folder = "/home/matlab/lslab/original_images"
command_to_run = """echo 'OK'
# Latest added file in the directory
name=`ls ./original_images -t | head -n1`
# Get timestamp from original image
created=`identify -verbose ./original_images/$name | grep 'create'`
created=${created#*:}
created=${created#*:}
echo ${created}

# Detect person and Crop the region
cd /home/matlab/darknet
./darknet detect cfg/yolo.cfg yolo.weights /home/matlab/lslab/original_images/$name  -thresh 0.6
echo 'darknet done'
cd /home/matlab/lslab

# Change name of cropped image
mv ../darknet/cropped.jpg ./cropped_images/$name
touch -d ${created} ./cropped_images/$name
echo $name ' changing time done'
"""

def get_drlist():
    return subprocess.check_output(["ls", folder]).decode('utf-8').strip().split("\n")

while True:
    drlist1 = get_drlist()
    time.sleep(2)
    drlist2 = get_drlist()
    if len(drlist2) > len(drlist1):
        subprocess.Popen(["/bin/bash", "-c", command_to_run])
