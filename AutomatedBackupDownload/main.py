import requests, os, json, sys
from tqdm import tqdm
from settings import Configuration, SfError
from colorama import Fore, Style

ROOT=os.path.dirname(os.path.abspath(__file__))

def print_error(message):
    print(f"{Fore.RED}ERROR: {message}{Style.RESET_ALL}")


def loadConfig():
    try:
        with open(os.path.join(ROOT, "config.json")) as config:
            c = json.load(config)
            config.close()
    except:
            print("#-ERROR NO CONTROLADO:", sys.exc_info()[0])
            raise

    return Configuration(c["username"],c["password"], c["security_token"], c["auth_url"],c["org_url"])


#CARGA DE DATOS DE LOGIN POR CONFIG
def getLoginXML(CONFIG):
    with open(os.path.join(ROOT, "login.xml"), "r") as loginXML:
        data = loginXML.read()
    data = data.replace("{{! USERNAME }}", CONFIG.USERNAME)
    data = data.replace("{{! PASSWORD }}", CONFIG.PASSWORD)
    data = data.replace("{{! SECURITY_TOKEN }}", CONFIG.SECURITY_TOKEN)
    return data

def login(CONFIG):
    headers = {
        "Content-Type" : "text/xml; charset=UTF-8",
        "SOAPAction": "login"
    }
    data = getLoginXML(CONFIG)
    r = requests.post(CONFIG.AUTH_URL, data=data, headers=headers)
    if r.status_code == 200:
        return r
    else:
        raise SfError(r.reason, r.text)

def headers(RESULT):
    return {
        'Cookie': "oid=" + RESULT.org_id() + "; sid=" + RESULT.session_id(),
        'X-SFDC-Session': RESULT.session_id()
    }

def getFileLink(RESULT, CONFIG):
    REQ_URL=CONFIG.ORG_URL + "/servlet/servlet.OrgExport"
    h = headers(RESULT)
    r = requests.get(REQ_URL, headers=h)
    if r.status_code == 200:
        if r.text is None:
            raise SfError('No File Found', 'Export Data Not Available')
        else:
            return r.text
    else:
        raise SfError(r.reason, r.status_code)

def downloadFile(LINK, RESULT, CONFIG):
    REQ_URL = CONFIG.ORG_URL + LINK
    fileName = LINK[(LINK.find('fileName') +9):(LINK.find('&'))]
    DIR = os.path.join(ROOT, "downloads")
    CHECK_FOLDER = os.path.isdir(DIR)
    if not CHECK_FOLDER:
        os.makedirs(DIR)
    Location = os.path.join(DIR, fileName)
    h = headers(RESULT)

    print('#-FileName--> ' + fileName)
    print('#-REQ_URL--> ' + REQ_URL.strip())
    base_url = "https://onnera.my.salesforce.com/"
    url_list = REQ_URL.strip().split('\n')
    url_list = [base_url + url if not url.startswith("http") else url for url in url_list]
    print('TOTAL DE ARCHIVOS A DESCARGAR -- ' + str(len(url_list)))

    for i, url in enumerate(url_list):
            print(f"POSICION[{i}] - {url}")
    return Location


def callHTTP(h,Location,url):
    try:
        with requests.get(url, headers=h, stream=True) as r:

            totalSize = int(r.headers.get('Content-Length', 0))
            progress = tqdm(total=totalSize, unit='iB', unit_scale=True)
            r.raise_for_status()
            with open(Location, 'wb') as archive:
                for chunk in r.iter_content(chunk_size=1024):
                    progress.update(len(chunk))
                    archive.write(chunk)
            progress.close()
        archive.close()
    except:
        print("#-ERROR NO CONTROLADO:", sys.exc_info()[0])
        raise
    return Location
