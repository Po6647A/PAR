import json
import os
import shutil
import argparse

import audio
import video
from pgr import PgrChart

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("chart", help='Path to your chart(json format)')
	parser.add_argument("music", help='Path to your music')
	parser.add_argument("Illustration", help='Path to your Illustration')
	parser.add_argument('-o',"--output", help='Path to your video file(Default: ./)')
	parser.add_argument('-f',"--fps", help='Video FPS (Default: 60)', type=int)
	parser.add_argument('-d',"--difficulty", help='Set to the Diffculty(Default: UnKnown Lv.?)')
	parser.add_argument('-n',"--name", help='Set to the Name(Default: UnKnown)')
	parser.add_argument('-t',"--text", help='Set to Combo Text(Default: AUTOPLAY)')
	args = parser.parse_args()
	combo_text = args.text or "AUTOPLAY"
	chart_path = args.chart
	music_path = args.music
	illustration_path = args.Illustration
	output_path = args.output or './'
	fps = args.fps or 60
	difficulty = args.difficulty or "Unknown Lv.?"
	name = args.name or "Unknown"
	
	workspace = os.path.join(output_path, 'workspace')
	if os.path.exists(workspace):
		shutil.rmtree(workspace)
	os.mkdir(workspace)
	chart = shutil.copy(chart_path, workspace)
	music = shutil.copy(music_path, workspace)
	ill = shutil.copy(illustration_path, workspace)
	
	with open(chart, 'r', encoding = 'utf-8') as f:
		chart = json.loads(f.read())
	chart = PgrChart(chart, (1920, 1080))
	
	music = audio.toWav(music)
	
	audio.processSoundEffect(music, chart)
	
	video.processAutoplay(chart, ill, music, fps, combo_text, output_path, 1920, 1080)
	
	