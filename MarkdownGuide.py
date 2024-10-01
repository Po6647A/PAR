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
		with open(os.path.join(versionDir, 'README.md'), 'w', encoding = 'utf-8') as main:
			for name, info in getInfos():
				path = os.path.join(versionDir, name)
				os.mkdir(path)
				music = os.path.join(musicPath, f'{name}.ogg')
				copy(music, path)
				Illustration = os.path.join(IllustrationPath, f'{name}.png')
				copy(Illustration, path)
				IllustrationLowRes = os.path.join(IllustrationLowResPath, f'{name}.png')
				rename(IllustrationLowRes, os.path.join(IllustrationLowResPath, f'{name}(Low).png'))
				copy(os.path.join(IllustrationLowResPath, f'{name}(Low).png'), path)
				IllustrationBlur = os.path.join(IllustrationBlurPath, f'{name}.png')
				rename(IllustrationBlur, os.path.join(IllustrationLowResPath, f'{name}(Blur).png'))
				copy(os.path.join(IllustrationLowResPath, f'{name}(Blur).png'), path)
				with open(os.path.join(path, 'README.md'), 'w', encoding = 'utf-8') as single:
					single.write(
						f'''
						# Phigros 版本/Phigros Version:  {version}
						
						- ### __曲名/Name:  {info['Name']}__
						
						- ### __作曲者/Composer:  {info['Composer']}__
						
						- ### __曲绘画师/Illustrator:  {info['Illustrator']}__
						
						- ### __曲绘/Illustration:  [下载/Download](./{name}.png)__
						
						- ### __音频/Music:  [下载/Download](./{name}.ogg)__
						
						- ### __曲绘(低质量)/IllustrationLowRes:  [下载/Download](./{name}(Low).png)__
						
						- ### __曲绘(模糊)/IllustrationBlur:  [下载/Download](./{name}(Blur).png)__
						'''
					)
					levels = ['EZ', 'HD', 'IN', 'AT']
					for index, level in enumerate(info['difficulty']):
						difficulty = levels[index]
						chartsPath = os.path.join(path, difficulty)
						os.mkdir(chartsPath)
						basename = os.path.join(resPath, f'Chart_{difficulty}', name)
						origchart = os.path.join(basename, '0.json')
						rpechart = os.path.join(basename, '0.rpe.json')
						phirachart = os.path.join(basename, '0.rpe.official.json')
						pez = os.path.join(phiraPath, difficulty, name + f'-{difficulty}.pez')
						phirapez = os.path.join(phiraPath, difficulty, name + f'-{difficulty}(Phira ver.).pez')
						rpepez = os.path.join(phiraPath, difficulty, name + f'-{difficulty}(RPE ver.).pez')
						copy(pez, chartsPath)
						copy(phirapez, chartsPath)
						copy(rpepez, chartsPath)
						copy(pez, os.path.join(chartsPath, f'{name}-{difficulty}.zip'))
						copy(phirapez, os.path.join(chartsPath, f'{name}-{difficulty}(Phira ver.).zip'))
						copy(rpepez, os.path.join(chartsPath, f'{name}-{difficulty}(RPE ver.).zip'))
						copy(origchart, chartsPath)
						copy(rpechart, chartsPath)
						copy(phirachart, chartsPath)
						PhichainProject = os.path.join(PhichainProjectPath, difficulty, name)
						with ZipFile(os.path.join(chartsPath, f'{name}-{difficulty}(PhichainProject ver.).zip'),'w') as f:
							zipwrite(f, os.path.join(PhichainProject, 'chart.json'))
							zipwrite(f, os.path.join(PhichainProject, 'meta.json'))
							zipwrite(f, os.path.join(PhichainProject, 'music.ogg'))
							zipwrite(f, os.path.join(PhichainProject, 'illustration.png'))
						single.write(
							f'''
							- ### __{level}谱面/{level} chart:  [查看/View](./{difficulty}/README.md)__
							'''
						)
						with open(os.path.join(chartsPath, 'README.md'),'w',encoding='utf-8') as chart:
							chart.write(
								f'''
								# Phigros 版本/Phigros Version:  {version}
								
								# __{info['Name']} - {level}__
								
								- ### __谱面文件(Pez格式)/Chart File(Pez Format):  [下载/Download](./{name}-{difficulty}.pez)__
								
								- ### __谱面文件(Zip格式)/Chart File(Zip Format):  [下载/Download](./{name }-{difficulty}.zip)__
								
								- ### __谱面文件(Pez格式)(Phira版本)/Chart File(Pez Format)(Phira ver.):   [下载/Download](./{name}-{difficulty}(Phira ver.).pez)__
								
								- ### __谱面文件(Zip格式)(Phira版本)/Chart File(Zip Format)(Phira ver.):   [下载/Download](./{name}-{difficulty}(Phira ver.).zip)__
								
								- ### __谱面文件(Pez格式)(RPE版本)/Chart File(Pez Format)(RPE ver.):   [下载/Download](./{name}-{difficulty}(RPE ver.).pez)__
								
								- ### __谱面文件(Zip格式)(RPE版本)/Chart File(Zip Format)(RPE ver.):   [下载/Download](./{name}-{difficulty}(RPE ver.).zip)__
								
								- ### __谱面文件(Zip格式)(Phichain版本)/Chart File(Phichain ver.):   [下载/Download](./{name}-{difficulty}(PhichainProject ver.).zip)__
								
								- ### __谱面文件(json格式)/Chart File(json Format)[下载/Download](./{name}.0.json)__
								
								- ### __谱面文件(json格式)(Phira版本)/Chart File(json Format)(Phira ver.)[下载/Download](./{name}.0.rpe.official.json)__
								
								- ### __谱面文件(json格式)(RPE版本)/Chart File(json Format)(RPE ver.)[下载/Download](./{name}.0.rpe.json)__
								'''
							)