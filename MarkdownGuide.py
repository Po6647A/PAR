import os
import shutil
import json
from zipfile import ZipFile

def getInfos():
	resPath = os.path.abspath('Phigros_Resource')
	infos = {}
	with open(os.path.join(resPath, 'info.tsv'), encoding = 'utf-8') as f:
		while True:
			line = f.readline()
			if not line:
				break
			line = line[:-1].split('\t')
			infos[line[0]] = {'Name': line[1], 'Composer': line[2], 'Illustrator': line[3], 'Charter': line[4:]}
			
	with open(os.path.join(resPath, 'difficulty.tsv'), encoding = 'utf-8') as f:
		while True:
			line = f.readline()
			if not line:
				break
			line = line[:-1].split('\t')
			infos[line[0]]['difficulty'] = line[1:]
	return infos.items()

def zipwrite(f, src):
	if os.path.exists(src):
		f.write(src)

def main(upload, release):
	resPath = os.path.abspath('Phigros_Resource')
	phiraPath = os.path.join(resPath, 'phira')
	musicPath = os.path.join(resPath, 'music')
	IllustrationPath = os.path.join(resPath, 'Illustration')
	IllustrationBlurPath = os.path.join(resPath, 'IllustrationBlur')
	IllustrationLowResPath = os.path.join(resPath, 'IllustrationLowRes')
	PhichainProjectPath = os.path.abspath('PhichainProject')
	with open(os.path.join('Phigros_Resource', 'manifest.json'), 'r', encoding = 'utf-8') as f:
		version = json.load(f)['version_name']
	downPath = f'''https://github.com/364hao/Test/releases/download/v{version}'''
	srcDir = os.path.join(os.path.abspath('src'))
	if not os.path.exists(srcDir):
		os.mkdir(srcDir)
	versionDir = os.path.join(srcDir, version)
	if not os.path.exists(os.path.abspath('book')):
		os.mkdir(os.path.abspath('book'))
	if not os.path.exists(versionDir):
		os.mkdir(versionDir)
		with open(os.path.join(versionDir, 'README.md'), 'w', encoding = 'utf-8') as commit:
			infos = getInfos()
			commit.write(
				f'''
				# Phigros 版本/Phigros Version:  {version}
				
				# 总计 {len(infos)} 曲目 /Total {len(infos)} songs
				'''
			)
			for name, info in infos:
				path = os.path.join(versionDir, name)
				os.mkdir(path)
				print(name, info)
				music = os.path.join(musicPath, f'{name}.ogg')
				upload(release, music)
				Illustration = os.path.join(IllustrationPath, f'{name}.png')
				upload(release, Illustration)
				IllustrationLowRes = os.path.join(IllustrationLowResPath, f'{name}.png')
				upload(release, IllustrationLowRes, f'{name}(Low).png')
				IllustrationBlur = os.path.join(IllustrationBlurPath, f'{name}.png')
				upload(release, IllustrationBlur, f'{name}(Blur).png')
				with open(os.path.join(path, 'README.md'), 'w', encoding = 'utf-8') as single:
					single.write(
						f'''
						# Phigros 版本/Phigros Version:  {version}
						
						- ### __曲名/Name:  {info['Name']}__
						
						- ### __作曲者/Composer:  {info['Composer']}__
						
						- ### __曲绘画师/Illustrator:  {info['Illustrator']}__
						
						- ### __曲绘/Illustration:  [下载/Download]({downPath}/{name}.png)__
						
						- ### __音频/Music:  [下载/Download]({downPath}/{name}.ogg)__
						
						- ### __曲绘(低质量)/IllustrationLowRes:  [下载/Download]({downPath}/{name}(Low).png)__
						
						- ### __曲绘(模糊)/IllustrationBlur:  [下载/Download]({downPath}/{name}(Blur).png)__
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
						upload(release, pez)
						upload(release, pez, f'{name}-{difficulty}.zip')
						upload(release, phirapez)
						upload(release, phirapez, f'{name}-{difficulty}(Phira ver.).zip')
						upload(release, rpepez)
						upload(release, rpepez, f'{name}-{difficulty}(RPE ver.).zip')
						upload(release, origchart, f'{name}-{difficulty}.json')
						upload(release, rpechart, f'{name}-{difficulty}(RPE ver.).json')
						upload(release, phirachart, f'{name}-{difficulty}(Phira ver.).json')
						PhichainProject = os.path.join(PhichainProjectPath, difficulty, name)
						Phichain = os.path.join(chartsPath, f'{name}-{difficulty}(PhichainProject ver.).zip')
						with ZipFile(Phichain , 'w') as f:
							zipwrite(f, os.path.join(PhichainProject, 'chart.json'))
							zipwrite(f, os.path.join(PhichainProject, 'meta.json'))
							zipwrite(f, os.path.join(PhichainProject, 'music.ogg'))
							zipwrite(f, os.path.join(PhichainProject, 'illustration.png'))
						upload(release, Phichain)
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
								
								- ### __谱面文件(Pez格式)/Chart File(Pez Format):  [下载/Download]({downPath}/{name}-{difficulty}.pez)__
								
								- ### __谱面文件(Zip格式)/Chart File(Zip Format):  [下载/Download]({downPath}/{name}-{difficulty}.zip)__
								
								- ### __谱面文件(Pez格式)(Phira版本)/Chart File(Pez Format)(Phira ver.):   [下载/Download]({downPath}/{name}-{difficulty}(Phira ver.).pez)__
								
								- ### __谱面文件(Zip格式)(Phira版本)/Chart File(Zip Format)(Phira ver.):   [下载/Download]({downPath}/{name}-{difficulty}(Phira ver.).zip)__
								
								- ### __谱面文件(Pez格式)(RPE版本)/Chart File(Pez Format)(RPE ver.):   [下载/Download]({downPath}/{name}-{difficulty}(RPE ver.).pez)__
								
								- ### __谱面文件(Zip格式)(RPE版本)/Chart File(Zip Format)(RPE ver.):   [下载/Download]({downPath}/{name}-{difficulty}(RPE ver.).zip)__
								
								- ### __谱面文件(Zip格式)(Phichain版本)/Chart File(Phichain ver.):   [下载/Download]({downPath}/{name}-{difficulty}(PhichainProject ver.).zip)__
								
								- ### __谱面文件(json格式)/Chart File(json Format)[下载/Download]({downPath}/{name}-{difficulty}.json)__
								
								- ### __谱面文件(json格式)(RPE版本)/Chart File(json Format)(RPE ver.)[下载/Download]({downPath}/{name}-{difficulty}(RPE ver.).json)__
								
								- ### __谱面文件(json格式)(Phira版本)/Chart File(json Format)(Phira ver.)[下载/Download]({downPath}/{name}-{difficulty}(Phira ver.).json)__
								
								'''
							)
				commit.write(
					f'''
					
					### [{name}-{info['Composer']}](./{name}/README.md)
					
					'''
				)
		with open(os.path.join('src', 'SUMMARY.md'), 'a', encoding = 'utf-8') as main:
			main.write(
				f'''
				- [{version}](./{version}/README.md)
				
				'''
			)