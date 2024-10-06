import audio
import video
import json
import os
import subprocess
from zipfile import ZipFile
from rich.progress import track
from pgr import PgrChart

def single(chart, music):
	with open(chart, 'r', encoding = 'utf-8') as f:
		chart = json.loads(f.read())
	chart = PgrChart(chart)
	music = audio.toWav(music)
	audio.processSoundEffect(music, chart)
	return music

resourceDir = os.path.abspath('PhichainProject')

EZ = os.path.join(resourceDir, "EZ")
HD = os.path.join(resourceDir, "HD")
IN = os.path.join(resourceDir, "IN")
AT = os.path.join(resourceDir, "AT")
processes = []
for difficultyDir in [EZ, HD, IN, AT]:
	for chartName in os.listdir(difficultyDir):
		print(chartName)
		chartPath = os.path.join(difficultyDir, chartName)
		chart = os.path.join(chartPath, 'chart.json')
		music = os.path.join(chartPath, 'music.ogg')
		music = single(chart, music)
		video = os.path.join(chartPath, 'output_video.mp4')
		command = [
			'ffmpeg',
			'-i',
			music,
			'-i',
			video,
			os.path.join(chartPath, 'video.mp4')
		]
		processes.append(subprocess.Popen(command))
for p in processes:
	p.wait()