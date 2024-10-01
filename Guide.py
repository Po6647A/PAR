import os
import shutil

def getInfos():
	resPath = os.path.abspath('Phigros_Resource')
	infos = {}
	with open(os.path.join(resPath, 'info.tsv'), encoding = 'utf8') as f:
		while True:
			line = f.readline()
			if not line:
				break
			line = line[:-1].split('\t')
			infos[line[0]] = {'Name': line[1], 'Composer': line[2], 'Illustrator': line[3], 'Charter': line[4:]}
			
	with open(os.path.join(resPath, 'difficulty.tsv'), encoding = 'utf8') as f:
		while True:
			line = f.readline()
			if not line:
				break
			line = line[:-1].split('\t')
			infos[line[0]]['difficulty'] = line[1:]
	return infos.items()

def copy(src, dst):
	if os.path.exists(src):
		shutil.copy(src, dst)

if __name__ =='__main__':
	resPath = os.path.abspath('Phigros_Resource')
	phiraPath = os.path.join(resPath, 'phira')
	if not os.path.exists('docs'):
		os.mkdir('docs')
	with open(os.path.join('Phigros_Resource', 'manifest.json'), 'r', encoding = 'utf-8') as f:
		version = json.load(f)['version_name']
	versionDir = os.path.join(os.path.abspath('docs'), version)
	if not os.path.exists(versionDir):
		os.mkdir(versionDir)
		with open('Main.md', 'w', encoding = 'utf-8') as main:
			for name, info in getInfos():
				path = os.path.join(versionDir, name)
				os.mkdir(path)
				copy()
				for difficulty in 
			
