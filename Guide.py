import os

if __name__ =='__main__':
	if not os.path.exists('docs'):
		os.mkdir('docs')
	with open(os.path.join('Phigros_Resource', 'manifest.json'), 'r', encoding = 'utf-8') as f:
		version = json.load(f)['version_name']
	versionDir = os.path.join('docs', version)
	if not os.path.exists(versionDir):
		os.mkdir(versionDir)
		
		with open("Main.md", "w", encoding = "utf-8") as f:
			pass