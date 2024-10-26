import os
import struct
import sys
import UnityPy
import zipfile
import infolib

class ByteReader:
    def __init__(self, data: bytes):
        self.data = data
        self.position = 0
        self.d = {bool: self.readBool, int: self.readInt, float: self.readFloat, str: self.readString}
    
    def readBool(self):
        self.position += 4
        return self.data[self.position - 4] == 0

    def readInt(self):
        self.position += 4
        return self.data[self.position - 4] ^ self.data[self.position - 3] << 8

    def readFloat(self):
        self.position += 4
        return struct.unpack("f", self.data[self.position - 4:self.position])[0]

    def readString(self):
        length = self.readInt()
        result = self.data[self.position:self.position + length].decode()
        self.position += length // 4 * 4
        if length % 4 != 0:
            self.position += 4
        return result
    
    def readClass(self, clazz):
        obj = clazz()
        for key, t in clazz.__annotations__.items():
            if type(t) == type:
                if t in (bool, int, float, str):
                    setattr(obj, key, self.d[t]())
                else:
                    setattr(obj, key, self.readClass(t))
            else:
                l = []
                t = t.__args__[0]
                for _ in range(self.readInt()):
                    if t in (bool, int, float, str):
                        l.append(self.d[t]())
                    else:
                        l.append(self.readClass(t))
                setattr(obj, key, l)
        return obj

def getInfo(path):
    env = UnityPy.Environment()
    with zipfile.ZipFile(path) as apk:
        with apk.open("assets/bin/Data/globalgamemanagers.assets") as f:
            env.load_file(f.read(), name="assets/bin/Data/globalgamemanagers.assets")
        with apk.open("assets/bin/Data/level0") as f:
            env.load_file(f.read())
    for obj in env.objects:
        if obj.type.name != "MonoBehaviour":
            continue
        data = obj.read()
        if data.m_Script.get_obj().read().name == "GameInformation":
            information = data.raw_data.tobytes()
        elif data.m_Script.get_obj().read().name == "GetCollectionControl":
            collection = data.raw_data.tobytes()
        elif data.m_Script.get_obj().read().name == "TipsProvider":
            tips = data.raw_data.tobytes()

    reader = ByteReader(information)
    reader.position = information.index(b"\x16\x00\x00\x00Glaciaxion.SunsetRay.0\x00\x00\n") - 4

    difficulty = []
    table = []
    for _ in range(3):
        for _ in range(reader.readInt()):
            songItem = reader.readClass(infolib.SongsItem)
            if len(songItem.difficulty) == 5:
                songItem.difficulty.pop()
                songItem.charter.pop()
            if songItem.difficulty[-1] == 0.0:
                songItem.difficulty.pop()
                songItem.charter.pop()
            for i in range(len(songItem.difficulty)):
                songItem.difficulty[i] = str(round(songItem.difficulty[i], 1))
            difficulty.append(
                [songItem.songsId] + songItem.difficulty
            )
            table.append(
                (
                    songItem.songsId,
                    songItem.songsName,
                    songItem.composer,
                    songItem.illustrator,
                    songItem.previewTime,
                    songItem.previewEndTime,
                    *songItem.charter,
                )
            )
    for i in range(reader.readInt()):
        reader.readClass(infolib.SongsItem)

    with open("info/difficulty.txt", "w", encoding = "utf-8") as f:
        for item in difficulty:
            for t in item:
                f.write(f"{t}\t")
            f.write('\n')

    with open("info/info.txt", "w", encoding = "utf-8") as f:
        for item in table:
            for t in item:
                f.write(f"{t}\t")
            f.write('\n')

    reader = ByteReader(collection)

    D = {}
    for i in range(reader.readInt()):
        item = reader.readClass(infolib.CollectionItemIndex)
        if item.key in D:
            D[item.key][1] = item.subIndex
        else:
            D[item.key] = [item.multiLanguageTitle.chinese, item.subIndex]

    with open("info/collection.txt", "w", encoding = "utf-8") as f:
        for key, value in D.items():
            f.write(f"{key}\t{value[0]}\t{value[1]}\n")

    with open("info/avatar.txt", "w", encoding = "utf-8") as avatar:
        for i in range(reader.readInt()):
            item = reader.readClass(infolib.AvatarInfo)
            avatar.write(f"{item.name}\t{item.addressableKey[7:]}\n")

    reader = ByteReader(tips[8:])

    with open("info/tips.txt", "w", encoding = "utf-8") as f:
        for i in range(reader.readInt()):
            f.write(reader.readString()+"\n")

def main(path = 'com.PigeonGames.Phigros.apk'):
    if not os.path.isdir("info"):
        os.mkdir("info")
    getInfo(path)

if __name__ == "__main__":
    main(sys.argv[1])