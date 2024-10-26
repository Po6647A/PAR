import hashlib
import json
import random
import string
import time
import urllib.parse
import urllib.request
import uuid
import requests

sample = string.ascii_lowercase + string.digits

# Phigros app id = 165287
def taptap(appid = 165287):
    uid = uuid.uuid4()
    X_UA = "V=1&PN=TapTap&VN_CODE=206012000&LOC=CN&LANG=zh_CN&CH=default&UID=%s" % uid
    
    req = urllib.request.Request(
        "https://api.taptapdada.com/app/v2/detail-by-id/%d?X-UA=%s" % (appid, urllib.parse.quote(X_UA)),
        headers={"User-Agent": "okhttp/3.12.1"}
    )
    with urllib.request.urlopen(req) as response:
        r = json.load(response)
    print(r["data"]["download"])
    apkid = r["data"]["download"]["apk_id"]
    

    nonce = "".join(random.sample(sample, 5))
    t = int(time.time())
    byte = "X-UA=%s&end_point=d1&id=%d&node=%s&nonce=%s&time=%sPeCkE6Fu0B10Vm9BKfPfANwCUAn5POcs" % (X_UA, apkid, uid, nonce, t)
    md5 = hashlib.md5(byte.encode()).hexdigest()
    body = "sign=%s&node=%s&time=%s&id=%d&nonce=%s&end_point=d1" % (md5, uid, t, apkid, nonce)

    req = urllib.request.Request(
        "https://api.taptapdada.com/apk/v1/detail?X-UA=" + urllib.parse.quote(X_UA),
        body.encode(),
        {"User-Agent": "okhttp/3.12.1"}
    )
    with urllib.request.urlopen(req) as response:
        return json.load(response)

def main(path = 'com.PigeonGames.Phigros.apk'):
    session = requests.Session()
    session.headers.update({"User-Agent": "okhttp/3.12.1"})
    x = taptap()['data']['apk']
    with open(path, 'wb') as f:
        f.write(session.get(x['download']).content)
    return x['version_name']

if __name__ == "__main__":
    main(sys.argv[1])