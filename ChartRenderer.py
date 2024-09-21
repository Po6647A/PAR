import subprocess
import os
import shutil


makerPath = os.path.abspath('phichain-renderer.exe')
resourceDir = os.path.abspath('Phigros_Resource')
PhiraDir = os.path.join(resourceDir, "phira")

processes = []
for difficulty in os.listdir(PhiraDir):
	if difficulty == 'AT':
		difficultyDir = os.path.join(PhiraDir, difficulty)
		for chartName in os.listdir(difficultyDir):
			if chartName.endswith('-rpe.pez'):
				chartPath = os.path.join(difficultyDir, chartName)
				processes.append(
					subprocess.Popen(
						[makerPath, chartPath]
					)
				)
for p in processes:
	p.wait()