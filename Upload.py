from github import Github
import json
import os

def exist_release(repo, tag_name):
    releases = repo.get_releases()
    for release in releases:
        if release.tag_name == tag_name:
            return True
    return False

def upload(release, filepath):
    release.upload_asset(
        path = filepath,
        label = os.path.basename(filepath),
        content_type = "application/octet-stream"
    )
if __name__ == '__main__':
    g = Github(os.environ.get('GITHUB_TOKEN'))
    repo = g.get_repo("364hao/Test")
    resDir = os.path.abspath('Phigros_Resource')
    with open(os.path.join(resDir, 'manifest.json'), 'r', encoding = 'utf-8') as f:
        version = 'v' + json.load(f)['version_name']
        if not exist_release(repo, version):
            release = repo.create_git_release(
                tag = version,
                name = f'Version {version} full assests',
                message = "From Apkpure, Github Action bot Generate"
            )
            upload(os.path.join(resDir, 'icon.png'))
            upload(os.path.join(resDir, 'difficulty.tsv'))
            upload(os.path.join(resDir, 'collection.tsv'))
            upload(os.path.join(resDir, 'avatar.txt'))
            upload(os.path.join(resDir, 'illustration.txt'))
            upload(os.path.join(resDir, 'info.tsv'))
            upload(os.path.join(resDir, 'music-info.json'))
            upload(os.path.join(resDir, 'tips.txt'))
            upload(os.path.join(resDir, 'single.txt'))
            