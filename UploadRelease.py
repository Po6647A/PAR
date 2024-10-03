import json
import os
import subprocess
from MarkdownGuide import main

def upload(release, filepath, v, name = None):
    if os.path.exists(filepath):
        if name != None:
            newpath = os.path.join(os.path.dirname(filepath), name)
            os.rename(filepath, newpath)
            filepath = newpath
        subprocess.Popen(
            [
                'gh',
                'release',
                'upload',
                f'v{v}',
                f'{filepath}',
                '--name',
                f'{name}'
            ]
        )
if __name__ == '__main__':
    resDir = os.path.abspath('Phigros_Resource')
    with open(os.path.join(resDir, 'manifest.json'), 'r', encoding = 'utf-8') as f:
        version = json.load(f)['version_name']
    try:
        subprocess.run(
            [
                'gh', 
                'release', 
                'create',
                f'v{version}', 
                '--title', 
                f'Version {version} full assests',
                '--notes',
                'From Apkpure, Github Action bot Generate'
            ]
        )
        upload(r, os.path.join(resDir, 'icon.png'), version)
        upload(r, os.path.join(resDir, 'difficulty.tsv'), version)
        upload(r, os.path.join(resDir, 'collection.tsv'), version)
        upload(r, os.path.join(resDir, 'avatar.txt'), version)
        upload(r, os.path.join(resDir, 'illustration.txt'), version)
        upload(r, os.path.join(resDir, 'info.tsv'), version)
        upload(r, os.path.join(resDir, 'music-info.json'), version)
        upload(r, os.path.join(resDir, 'tips.txt'), version)
        upload(r, os.path.join(resDir, 'single.txt'), version)
        main(upload, r)
    except:
        pass