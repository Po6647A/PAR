import subprocess
import os

converter = os.path.abspath('phichain-converter')
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
		processes.append(subprocess.Popen([converter, '--input', 'official', '--output', 'phichain', chartPath], shell = True))
for p in processes:
	p.wait()
	