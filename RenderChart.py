import subprocess
import time
import os
import sys
import shutil
from zipfile import ZipFile
from rich.progress import track
subprocess.Popen('x11vnc -display :1 -nopw -shared',shell = True)
time.sleep(1)


resourceDir = os.path.abspath('PhichainProject')
renderer = os.path.abspath('phichain-v0.4.1+build.383-x86_64-unknown-linux-gnu/phichain-renderer')

processes = []

EZ = os.path.join(resourceDir, "EZ")
HD = os.path.join(resourceDir, "HD")
IN = os.path.join(resourceDir, "IN")
AT = os.path.join(resourceDir, "AT")
for difficultyDir in [EZ, HD, IN, AT]:
	for chartName in os.listdir(difficultyDir):
		print(chartName)
		chartPath = os.path.join(difficultyDir, chartName)
		command = [
			renderer, 
			chartPath,
			'--fc-ap-indicator',
			'--output',
			os.path.join(chartPath, 'output_video.mp4')
		]
		processes.append(subprocess.Popen(command))
for p in processes:
	p.wait()
	