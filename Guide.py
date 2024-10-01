import os
import shutil
from zipfile import ZipFile

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
def rename(src, dst):
	if os.path.exists(src):
		os.rename(src, dst)
def zipwrite(f, src):
	if os.path.exists(src):
		f.write(src)

if __name__ =='__main__':
	resPath = os.path.abspath('Phigros_Resource')
	phiraPath = os.path.join(resPath, 'phira')
	musicPath = os.path.join(resPath, 'music')
	IllustrationPath = os.path.join(resPath, 'Illustration')
	IllustrationBlurPath = os.path.join(resPath, 'IllustrationBlur')
	IllustrationLowResPath = os.path.join(resPath, 'IllustrationLowRes')
	PhichainProjectPath = os.path.abspath('PhichainProject')
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
				with open(os.path.join(path, 'README.md'))
				music = os.path.join(musicPath, f'{name}.ogg')
				copy(music, path)
				Illustration = os.path.join(IllustrationPath, f'{name}.png')
				copy(Illustration, path)
				IllustrationLowRes = os.path.join(IllustrationLowResPath, f'{name}.png')
				copy(IllustrationLowRes, path)
				IllustrationBlur = os.path.join(IllustrationBlurPath, f'{name}.png')
				copy(IllustrationBlur, path)
				for index, difficulty in enumerate(info["difficulty"]):
					chartsPath = os.path.join(path, difficulty)
					os.mkdir(chartsPath)
					basename = os.path.join(resPath, f'Chart_{difficulty}', name)
					origchart = os.path.join(basename, '0.json')
					rpechart = os.path.join(basename, '0.rpe.json')
					phirachart = os.path.join(basename, '0.rpe.official.json')
					pez = os.path.join(phiraPath, difficulty, name + f'-{difficulty}.pez')
					phirapez = os.path.join(phiraPath, difficulty, name + f'-{difficulty}(Phira ver.).pez')
					copy(pez, chartsPath)
					copy(phirapez, chartsPath)
					copy(pez, os.path.join(chartsPath, f'{name}-{difficulty}.zip'))
					copy(phirapez, os.path.join(chartsPath, f'{name}-{difficulty}(Phira ver.).zip'))
					copy(origchart, chartsPath)
					copy(rpechart, chartsPath)
					copy(phirachart, chartsPath)
					PhichainProject = os.path.join(PhichainProjectPath, difficulty, name)
					with ZipFile(os.path.join(chartsPath, f'PhichainProject ver.zip'),'w') as f:
						zipwrite(f, os.path.join(PhichainProject, 'chart.json'))
						zipwrite(f, os.path.join(PhichainProject, 'meta.json'))
						zipwrite(f, os.path.join(PhichainProject, 'music.ogg'))
						zipwrite(f, os.path.join(PhichainProject, 'illustration.png'))
					