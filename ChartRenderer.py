import subprocess
import os
import shutil


makerPath = os.path.abspath('phichain-renderer.exe')
resourceDir = os.path.abspath('PhichainProject')

processes = []
for difficulty in os.listdir(resourceDir):
	difficultyDir = os.path.join(resourceDir, difficulty)
	for chartName in os.listdir(difficultyDir):
		chartPath = os.path.join(difficultyDir, chartName)
		processes.append(
			subprocess.Popen(
				makerPath+' '+chartPath+' --fc-ap-indicator'
			)
		)
for p in processes:
	p.wait()