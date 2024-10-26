import os
import shutil
import threading
from zipfile import ZipFile

def zipPez(id, index, difficulty, info):
    level = ["EZ", "HD", "IN", "AT"][index]
    pez_filename = f"{id}-{level}.pez"
    with ZipFile(f"phira/{pez_filename}", "w") as pez:
        pez.writestr(
            "info.txt",
            (f'''Name: {info['Name']}
Song: {id}.ogg
Picture: {id}.png
Chart: {id}.json
Level: {level} Lv.{difficulty}
Composer: {info['Composer']}
Illustrator: {info['Illustrator']}
Charter: {info['Charter'][index]}
previewStart: {info['previewStartTime']}
previewEnd: {info['previewEndTime']}''')
        )
        pez.write(f"chart/{id}/{level}.json", f"{id}.json")
        pez.write(f"IllustrationLowRes/{id}.png", f"{id}.png")
        pez.write(f"music/{id}.ogg", f"{id}.ogg")

def process(id, info):
    for index, difficulty in enumerate(info["difficulty"]):
        threading.Thread(target = zipPez, args = (id, index, difficulty, info,)).start()

def main():
    shutil.rmtree("phira", ignore_errors=True)
    os.makedirs("phira", exist_ok=True)

    infos = {}

    with open("info/info.txt", encoding = "utf-8") as f:
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


    with open("info/difficulty.txt", encoding = "utf-8") as f:
        while True:
            line = f.readline()
            if not line:
                break
            line = line.strip().split("\t")
            infos[line[0]]["difficulty"] = line[1:]


    for id, info in infos.items():
        print(f"{info['Name']} {info['Composer']}")
        threading.Thread(target = process, args = (id, info,)).start()
    
    print('Please Wait for Writing...')

if __name__ == '__main__':
    main()