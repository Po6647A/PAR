import base64
import json
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from queue import Queue
from UnityPy import Environment
from UnityPy.classes import AudioClip
from UnityPy.enums import ClassIDType
from zipfile import ZipFile
from fsb5 import FSB5


class ByteReader:
	def __init__(self, data):
		self.data = data
		self.position = 0

	def readInt(self):
		self.position += 4
		return self.data[self.position - 4] ^ self.data[self.position - 3] << 8 ^ self.data[self.position - 2] << 16


def writefile(item):
	path, res = item
	print(path)
	if type(res) == BytesIO:
		with res:
			with open(path, "wb") as f:
				f.write(res.getbuffer())
	else:
		with open(path, "wb") as f:
			f.write(res)

def outfile():
	while True:
		item = queue_in.get()
		if item == None:
			break
		else:
			threading.Thread(target = writefile, args = (item,)).start()


def save_image(path, image):
	bytesIO = BytesIO()
	image.save(bytesIO, "png")
	queue_in.put((path, bytesIO))


def save_music(path, music: AudioClip):
	fsb = FSB5(music.m_AudioData)
	rebuilt_sample = fsb.rebuild_sample(fsb.samples[0])
	queue_in.put((path, rebuilt_sample))


classes = ClassIDType.TextAsset, ClassIDType.Sprite, ClassIDType.AudioClip


def save(key, entry):
	obj = entry.get_filtered_objects(classes)
	obj = next(obj).read()
	if key[:7] == "avatar.":
		key = key[7:]
		if key != "Cipher1":
			key = avatar[key]
		bytesIO = BytesIO()
		obj.image.save(bytesIO, "png")
		queue_in.put((f"avatar/{key}.png", bytesIO))
	elif key[-14:-7] == "/Chart_" and key[-5:] == ".json":
		p = "chart/" + key[:-14]
		if not os.path.exists(p):
			os.mkdir(p)
		queue_in.put((f"chart/{key[:-14]}/{key[-7:-5]}.json", obj.script))
	elif key[-23:] == ".0/IllustrationBlur.png":
		key = key[:-23]
		bytesIO = BytesIO()
		obj.image.save(bytesIO, "png")
		queue_in.put((f"illustrationBlur/{key}.png", bytesIO))
	elif key[-25:] == ".0/IllustrationLowRes.png":
		key = key[:-25]
		pool.submit(save_image, f"illustrationLowRes/{key}.0.png", obj.image)
	elif key[-19:] == ".0/Illustration.png":
		key = key[:-19]
		pool.submit(save_image, f"illustration/{key}.0.png", obj.image)
	elif key[-12:] == ".0/music.wav":
		key = key[:-12]
		pool.submit(save_music, f"music/{key}.0.ogg", obj)


def run(path):
	with ZipFile(path) as apk:
		with apk.open("assets/aa/catalog.json") as f:
			data = json.load(f)

	key = base64.b64decode(data["m_KeyDataString"])
	bucket = base64.b64decode(data["m_BucketDataString"])
	entry = base64.b64decode(data["m_EntryDataString"])

	table = []
	reader = ByteReader(bucket)
	
	for _ in range(reader.readInt()):
		key_position = reader.readInt()
		key_type = key[key_position]
		key_position += 1
		if key_type == 0:
			length = key[key_position]
			key_position += 4
			key_value = key[key_position:key_position + length].decode()
		elif key_type == 1:
			length = key[key_position]
			key_position += 4
			key_value = key[key_position:key_position + length].decode("utf16")
		elif key_type == 4:
			key_value = key[key_position]
		else:
			raise BaseException(key_position, key_type)
		for i in range(reader.readInt()):
			entry_position = reader.readInt()
			entry_value = entry[4 + 28 * entry_position:4 + 28 * entry_position + 28]
			entry_value = entry_value[8] ^ entry_value[9] << 8
		table.append([key_value, entry_value])
	
	for i in range(len(table)):
		if table[i][1] != 65535:
			table[i][1] = table[table[i][1]][0]
	
	for i in range(len(table) - 1, -1, -1):
		if type(table[i][0]) == int or table[i][0][:15] == "Assets/Tracks/#" or table[i][0][:14] != "Assets/Tracks/" and \
				table[i][0][:7] != "avatar.":
			del table[i]
		elif table[i][0][:14] == "Assets/Tracks/":
			table[i][0] = table[i][0][14:]

	global avatar, pool
	avatar = {}
	with open("info/avatar.txt", encoding="utf-8") as f:
		line = f.readline()[:-1]
		while line:
			l = line.split('\t')
			avatar[l[1]] = l[0]
			line = f.readline()[:-1]

	thread = threading.Thread(target = outfile)
	thread.start()
	with ThreadPoolExecutor(10) as pool:
		with ZipFile(path) as apk:
			for key, entry in table:
				env = Environment()
				env.load_file(apk.read(f"assets/aa/Android/{entry}"), name = key)
				for ikey, ientry in env.files.items():
					save(ikey, ientry)
	queue_in.put(None)
	thread.join()

def main(path = 'com.PigeonGames.Phigros.apk'):
	global queue_in, queue_out
	queue_out = Queue()
	queue_in = Queue()
	for directory in ("avatar", "chart", "illustrationBlur", "illustrationLowRes", "illustration", "music"):
		if not os.path.isdir(directory):
			os.mkdir(directory)
	run(path)

if __name__ == "__main__":
	main(path = sys.argv[1])