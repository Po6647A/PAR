import subprocess
import os

maker = ".\\PhigrosPlayer\\OutputVideo.py"
resourceDir = os.path.abspath('Phigros_Resource')
PhiraDir = os.path.join(resourceDir, "phira")
for difficulty in os.listdir(PhiraDir):
	difficultyDir = os.path.join(PhiraDir, difficulty)
	for chartName in os.listdir(difficultyDir):
		print(chartName)
		chartPath = os.path.join(difficultyDir, chartName)
		subprocess.Popen(
			f'python {maker} {chartPath} {difficultyDir} --fps 144', 
			stdout = subprocess.DEVNULL,
			stderr = subprocess.DEVNULL
		)
