import requests
import zipfile

def zip_file(filename):
    zipname = filename.replace(".csv", ".zip")
    with zipfile.ZipFile(zipname, 'w') as z:
        z.write(filename)
    return zipname

def upload(zipname):
    url = "http://你的服务器IP:5000/upload"
    try:
        files = {"file": open(zipname, "rb")}
        requests.post(url, files=files, timeout=10)
        return True
    except:
        return False