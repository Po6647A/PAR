from collections import defaultdict
import os
from textwrap import dedent
import json

def getinfos(verp):
	infos = {}
	with open(f'{verp}/info/info.txt', encoding = "utf-8") as f:
		while True:
			line = f.readline()
			if not line:
				break
			line = line.strip().split("\t")
			infos[line[0]] = {
				"Name": line[1],
				"Composer": line[2],
				"Illustrator": line[3],
				"previewStartTime": line[4],
				"previewEndTime": line[5],
				"Charter": line[6:],
			}
	with open(f'{verp}/info/difficulty.txt', encoding = "utf-8") as f:
		while True:
			line = f.readline()
			if not line:
				break
			line = line.strip().split("\t")
			infos[line[0]]["difficulty"] = line[1:]
	return infos
	
def main():
	srcp = os.path.abspath('src')
	if not os.path.exists(srcp):
		os.mkdir(srcp)
	assestp = os.path.abspath('assests')
	repo = os.environ.get('GITHUB_REPOSITORY')
	for ver in os.listdir(assestp):
		mdp = os.path.join(srcp, ver)
		if not os.path.exists(mdp):
			with open(os.path.join('src', 'SUMMARY.md'), 'a', encoding = 'utf-8') as m:
				m.write(
f'''
- [Version {ver}](./{ver}/SUMMARY.md)

'''
				)
				os.mkdir(mdp)
				verp = os.path.join(assestp, ver)
				if not os.path.exists(f'{verp}/uploadict.json'):
					continue
				with open(f'{verp}/uploadict.json', 'r', encoding='utf-8') as f:
					uploadict = defaultdict(lambda: "0")
					for key, value in json.load(f).items():
						uploadict[key] = value
				with open(f'{mdp}/SUMMARY.md', 'w', encoding = 'utf-8') as summary:
					summary.write(
					f'''
# Phigros 版本/Phigros Version:  {ver}

- ## 总计 {len(os.listdir(f'{verp}/music'))} 曲目 /Total {len(os.listdir(f'{verp}/music'))} songs

- ## 总计 {len(os.listdir(f'{verp}/chart'))} 谱面 /Total {len(os.listdir(f'{verp}/chart'))} charts

- ## 总计 {len(os.listdir(f'{verp}/avatar'))} 头像 /Total {len(os.listdir(f'{verp}/avatar'))} avatars

- ## 总计 {len(os.listdir(f'{verp}/avatar'))} 头像 /Total {len(os.listdir(f'{verp}/avatar'))} avatars

'''
					)
					with open(f'{verp}/info/tips.txt', 'r', encoding = 'utf-8') as f:
						t = sum(1 for _ in f)
						summary.write(
f'''
- ## 总计 {t} tips /Total {t} tips

''')
					with open(f'{verp}/info/collection.txt', 'r', encoding = 'utf-8') as f:
						t = sum(1 for _ in f)
						summary.write(
f'''
- ## 总计 {t} 收藏品 /Total {t} collections

''')
					summary.write(
f'''
- ## 安装包/Apk [下载/Download](https://github.com/{repo}/releases/download/{ver}/{uploadict[f"[Package]Phigros.apk"]})

''')
					info = getinfos(verp)
					for t in os.listdir(f'{verp}/chart'):
						if not t in info:
							continue
						os.mkdir(f'{mdp}/{t}')
						with open(f'{mdp}/{t}/README.md', 'w', encoding = 'utf-8') as sg:
							sg.write(
f'''
# Phigros 版本/Phigros Version:  {ver}

- ### __曲名/Name:  {info[t]['Name']}__

- ### __作曲者/Composer:  {info[t]['Composer']}__

- ### __曲绘画师/Illustrator:  {info[t]['Illustrator']}__

- ### __曲绘/Illustration:  [下载/Download](https://github.com/{repo}/releases/download/{ver}/{uploadict[f"[Illustration]{t}.png"]})__

- ### __音频/Music:  [下载/Download](https://github.com/{repo}/releases/download/{ver}/{uploadict[f"[Music]{t}.ogg"]})__

- ### __曲绘(低质量)/IllustrationLowRes:  [下载/Download](https://github.com/{repo}/releases/download/{ver}/{uploadict[f"[IllustrationLowRes]{t}.png"]})__

- ### __曲绘(模糊)/IllustrationBlur:  [下载/Download](https://github.com/{repo}/releases/download/{ver}/{uploadict[f"[IllustrationBlur]{t}.png"]})__

'''
							)
							m.write(
f'''
  - [{info[t]['Name']}](./{ver}/{t}/README.md)
'''
							)
							for p in os.listdir(f'{verp}/chart/{t}'):
								pn, _ = os.path.splitext(p)
								m.write(
f'''
	- [{pn}](./{ver}/{t}/{p}/README.md)
'''
								)
								index = ['EZ', 'HD', 'IN', 'AT'].index(pn)
								os.mkdir(f'{mdp}/{t}/{p}')
								sg.write(
f'''
- ### __{pn}谱面/{pn} chart:  [查看/View](./{p}/index.html)__
'''
								)
								with open(f'{mdp}/{t}/{p}/README.md', 'w', encoding = 'utf-8') as chart:
									chart.write(
f'''
# Phigros 版本/Phigros Version:  {ver}

# __{info[t]['Name']} - {info[t]['difficulty'][index]}__

- ### __谱面文件(Pez格式)/Chart File(Pez Format):  [下载/Download](https://github.com/{repo}/releases/download/{ver}/{uploadict[f"[Phira]{t}-{p}"]})__

- ### __谱面文件(json格式)/Chart File(json Format)[下载/Download](https://github.com/{repo}/releases/download/{ver}/{uploadict[f"[Chart-{p}]{t}.json"]})__

'''
								)
		else:
			print(f'Skip {ver}, exist')
if __name__ == '__main__':
	main()