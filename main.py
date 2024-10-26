from taptap import main as download
from gameInformation import main as info
from resource import main as res
from phira import main as phira
from format import main as format

def main():
	print('[1]Download Package')
	version = download()
	print('[2]Collect Information')
	info()
	print('[3]Extract Resource')
	res()
	print('[4]Pack PEZ')
	phira()
	print('[5]Format Data')
	format(version)

if __name__ == '__main__':
	main()