import os
import shutil

def main(version):
	if not os.path.exists('assests'):
		os.mkdir('assests')
	ver = os.path.join('assests', version)
	if not os.path.exists(ver):
		os.mkdir(ver)
	print('Move Phigros Package Path')
	shutil.move('com.PigeonGames.Phigros.apk', f'{ver}/Phigros.apk')
	print('Move Chart Path')
	shutil.move('chart', f'{ver}/chart')
	print('Move Illustration Path')
	shutil.move('illustration', f'{ver}/illustration')
	print('Move Music Path')
	shutil.move('music', f'{ver}/music')
	print('Move IllustrationBlur Path')
	shutil.move('illustrationBlur', f'{ver}/illustrationBlur')
	print('Move IllustrationLowRes Path')
	shutil.move('illustrationLowRes', f'{ver}/illustrationLowRes')
	print('Move Info Path')
	shutil.move('info', f'{ver}/info')
	print('Move Avatar Path')
	shutil.move('avatar', f'{ver}/avatar')
	print('Move Phira Path')
	shutil.move('phira', f'{ver}/phira')

if __name__ == '__main__':
	main(sys.argv[1])