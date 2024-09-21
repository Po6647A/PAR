import subprocess
import os
import shutil


makerPath = os.path.abspath('phira-render')
resourceDir = os.path.abspath('Phigros_Resource')
PhiraDir = os.path.join(resourceDir, "phira")

processes = []
for difficulty in os.listdir(PhiraDir):
	if difficulty == 'AT':
		difficultyDir = os.path.join(PhiraDir, difficulty)
		for chartName in os.listdir(difficultyDir):
			if chartName.endswith('-rpe.pez'):
				print(chartName)
				chartPath = os.path.join(difficultyDir, chartName)
				name, _ = os.path.splitext(chartName)
				makerdir = os.path.join(difficultyDir, name)
				shutil.copytree(makerPath, makerdir)
				maker = os.path.join(makerdir, 'phira-render', 'phira-render.exe')
				print(os.listdir(makerdir))
				print(maker, chartPath)
				processes.append(
					subprocess.Popen(
						maker+" "+chartPath
					)
				)
for p in processes:
	p.wait()