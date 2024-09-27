import os
import sys
import shutil
from zipfile import ZipFile
from rich.progress import track

levels = ["EZ", "HD", "IN", "AT"]

infos = {}

os.mkdir("PhichainProject")
for level in levels:
    os.mkdir(f"PhichainProject/{level}")

with open("Phigros_Resource/info.tsv", encoding = "utf8") as f:
    while True:
        line = f.readline()
        if not line:
            break
        line = line[:-1].split("\t")
        infos[line[0]] = {"Name": line[1], "Composer": line[2], "Illustrator": line[3], "Chater": line[4:]}
        
with open("Phigros_Resource/difficulty.tsv", encoding = "utf8") as f:
    while True:
        line = f.readline()
        if not line:
            break
        line = line[:-1].split("\t")
        infos[line[0]]["difficulty"] = line[1:]

for id, info in track(infos.items(), description = "WritingPhichainProject..."):
    for level in range(len(info["difficulty"])):
        baseDir = f"PhichainProject/{levels[level]}/{id}"
        os.mkdir(baseDir)
        with open(baseDir+"/meta.json", 'w', encoding = 'utf-8') as f:
            f.write("{")
            f.write(f'"composer": {info["Composer"]},')
            f.write(f'"charter": {info["Chater"][level]},')
            f.write(f'"illustrator": {info["Illustrator"]},')
            f.write(f'"name": {info["Name"]},')
            f.write(f'"level": {info["difficulty"][level]}')
            f.write("}")
        shutil.copy(f"Phigros_Resource/Chart_{levels[level]}/{id}.0.json", baseDir)
        os.rename(baseDir+f'\\{id}.json',"chart.json")
        shutil.copy(f"Phigros_Resource/Illustration/{id}.png", baseDir)
        os.rename(baseDir+f'\\{id}.png',"illustration.png")
        shutil.copy(f"Phigros_Resource/music/{id}.ogg", baseDir)
        os.rename(baseDir+f'\\{id}.ogg',"music.ogg")