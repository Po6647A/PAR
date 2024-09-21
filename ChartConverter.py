import subprocess
import os

converter = os.path.abspath('phichain-converter.exe')
resourceDir = os.path.abspath('Phigros_Resource')

processes = []

EZ = os.path.join(resourceDir, "Chart_EZ")
HD = os.path.join(resourceDir, "Chart_HD")
IN = os.path.join(resourceDir, "Chart_IN")
AT = os.path.join(resourceDir, "Chart_AT")
for difficultyDir in [EZ, HD, IN, AT]:
	for chartName in os.listdir(difficultyDir):
		print(chartName)
		chartPath = os.path.join(difficultyDir, chartName)
		processes.append(subprocess.Popen(converter+' --input official '+'--output rpe '+chartPath))
for p in processes:
    p.wait()
processes = []
for difficultyDir in [ AT]:
	for chartName in os.listdir(difficultyDir):
		name, extension = os.path.splitext(chartName)
		chartName = name + '.rpe' + extension
		print(chartName)
		chartPath = os.path.join(difficultyDir, chartName)
		processes.append(subprocess.Popen(converter+' --input rpe'+' --output official '+chartPath))
for p in processes:
    p.wait()
    