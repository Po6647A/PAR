import subprocess
import os

converter = os.path.abspath('phichain-v0.4.1+build.383-x86_64-unknown-linux-gnu/phichain-converter')
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
		processes.append(subprocess.Popen([converter, '--input', 'official', '--output', 'phichain', chartPath]))
for p in processes:
	p.wait()
	