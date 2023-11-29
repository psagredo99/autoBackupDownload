# main.py
import os
import json
import sys
import requests
from tqdm import tqdm
from settings import Configuration, SfError
from colorama import Fore, Style
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))


def print_error(message):
    print(f"{Fore.RED}ERROR: {message}{Style.RESET_ALL}")


def loadConfig():
    try:
        with open(os.path.join(ROOT, "config.json")) as config:
            c = json.load(config)
    except Exception as e:
        print("#-ERROR NO CONTROLADO:", e)
        raise

    return Configuration(c["username"], c["password"], c["security_token"], c["auth_url"], c["org_url"])


def get_login_xml(config):
    with open(os.path.join(ROOT, "login.xml"), "r") as login_xml:
        data = login_xml.read()

    data = data.replace("{{! USERNAME }}", config.USERNAME)
    data = data.replace("{{! PASSWORD }}", config.PASSWORD)
    data = data.replace("{{! SECURITY_TOKEN }}", config.SECURITY_TOKEN)

    return data


def login(config):
    headers = {
        "Content-Type": "text/xml; charset=UTF-8",
        "SOAPAction": "login"
    }
    data = get_login_xml(config)
    r = requests.post(config.AUTH_URL, data=data, headers=headers)

    if r.status_code == 200:
        print('#-Login OK')
        return r
    else:
        print('#-Login FAILED')
        raise SfError(r.reason, r.text)


def headers(RESULT):
    return {
        'Cookie': "oid=" + RESULT.org_id() + "; sid=" + RESULT.session_id(),
        'X-SFDC-Session': RESULT.session_id()
    }


def getFileLink(RESULT, CONFIG):
    REQ_URL = CONFIG.ORG_URL + "/servlet/servlet.OrgExport"
    h = headers(RESULT)
    r = requests.get(REQ_URL, headers=h)
    if r.status_code == 200:
        if r.text is None:
            print('#-Busqueda ruta FAILED')
            raise SfError('No File Found', 'Export Data Not Available')
        else:
            print('#-Busqueda ruta OK')
            return r.text
    else:
        raise SfError(r.reason, r.status_code)


def downloadFile(LINK, RESULT, CONFIG):
    REQ_URL = CONFIG.ORG_URL + LINK
    fileName = LINK[(LINK.find('fileName') + 9):(LINK.find('&'))]
    # 28-11 | Mod para ejecucion mensual
    # DIR = os.path.join(ROOT, "downloads")
    DIR = create_folder()
    Location = os.path.join(DIR, fileName)
    h = headers(RESULT)
    base_url = "https://alokabide.my.salesforce.com/"
    url_list = REQ_URL.strip().split('\n')
    TOTAL_FILES=len(url_list)
    print('#-TOTAL DE ARCHIVOS A DESCARGAR -- ' + str(TOTAL_FILES-1))
    if TOTAL_FILES >1:
        url_list = [base_url + url if not url.startswith("http") else url for url in url_list]

        downloaded_files = []
        for i, u in enumerate(url_list, start=1):
            print('PROCESO--> ' + str(i) + ' URL -- ' + u)
            new_location = os.path.join(DIR, f"file_{i}.zip")
            callHTTP(headers(RESULT), new_location, u)
            downloaded_files.append(new_location)
    else:
        print('#-SIN ARCHIVOS ZIP PARA DESCARGAR || CERRANDO PROCESO')

    return Location


def callHTTP(h, Location, url):
    print('########################################################################')
    print('########################################################################')
    print('########################################################################')
    print('\t#-DESCARGA EN PROCESO--> ' + url)
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


def create_folder():
    current_date = datetime.now()
    month_year = current_date.strftime("%B_%Y")
    folder_path = os.path.join(os.getcwd(), month_year)
    if os.path.exists(folder_path):
        print(f"#-Carpeta '{folder_path}' ya existe.")
    else:
        try:
            os.makedirs(folder_path)
            print(f"#- Carpeta de salida -- '{folder_path}'")
        except OSError as e:
            print(f"Error creating folder: {e}")
    return folder_path
