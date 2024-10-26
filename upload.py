import os
import json
from github import Github, Auth

def upload(p, name):
	global cnt
	if os.path.exists(p):
		_, ext = os.path.splitext(p)
		format = str(cnt)+ext
		r.upload_asset(path = p, name = format)
		cnt += 1
		uploadict[name] = format
		print(name)
	else:
		print(f'Skip {p}, Not Exist')

def main():
	global uploadict, cnt, r
	
	g = Github(auth = Auth.Token(os.environ.get('GITHUB_TOKEN')))
	repo = g.get_repo(os.environ.get('GITHUB_REPOSITORY'))
	
	assdir = os.path.abspath('assests')
	
	uploadict = {}
	cnt = 1
	
	for version in os.listdir(assdir):
		verdir = os.path.join(assdir, version)
		try:
			r = repo.create_git_release(
				tag = f'{version}',
				name = f'Version {version}',
				message = 'PAR Generated',
			)
			for avatar in os.listdir(f'{verdir}/avatar'):
				p = os.path.join(f'{verdir}/avatar', avatar)
				upload(
					p,
					f'[Avatar]{os.path.basename(p)}'
				)
			for chart in os.listdir(f'{verdir}/chart'):
				for t in os.listdir(f'{verdir}/chart/{chart}'):
					p = os.path.join(f'{verdir}/chart/{chart}', t)
					upload(
						p,
						f'[Chart-{t}]{chart}.json'
					)
			for illustration in os.listdir(f'{verdir}/illustration'):
				p = os.path.join(f'{verdir}/illustration', illustration)
				upload(
					p,
					f'[Illustration]{os.path.basename(p)}'
				)
			for illustrationBlur in os.listdir(f'{verdir}/illustrationBlur'):
				p = os.path.join(f'{verdir}/illustrationBlur', illustrationBlur)
				upload(
					p,
					f'[IllustrationBlur]{os.path.basename(p)}'
				)
			for illustrationLowRes in os.listdir(f'{verdir}/illustrationLowRes'):
				p = os.path.join(f'{verdir}/illustrationLowRes', illustrationLowRes)
				upload(
					p,
					f'[IllustrationLowRes]{os.path.basename(p)}'
				)
			for info in os.listdir(f'{verdir}/info'):
				p = os.path.join(f'{verdir}/info', info)
				upload(
					p,
					f'[Info]{os.path.basename(p)}'
				)
			for music in os.listdir(f'{verdir}/music'):
				p = os.path.join(f'{verdir}/music', music)
				upload(
					p,
					f'[Music]{os.path.basename(p)}'
				)
			for phira in os.listdir(f'{verdir}/phira'):
				p = os.path.join(f'{verdir}/phira', phira)
				upload(
					p,
					f'[Phira]{os.path.basename(p)}'
				)
			upload(
				f'{verdir}/Phigros.apk',
				'[Package]Phigros.apk'
			)
			print('Upload Completed')
			print(f'Total {cnt - 1} Assests')
			with open(f'{verdir}/uploadict.json', 'w', encoding = 'utf-8') as f:
				json.dump(uploadict, f, ensure_ascii = False, indent = 4)
		except Exception as e:
			print(e)
			print(f'Skip Version {version}')

if __name__ == '__main__':
	main()