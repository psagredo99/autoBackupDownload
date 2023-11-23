#Realizar carga de librerias 
from main import (
loadConfig,
login,
getFileLink,
downloadFile
)
from settings import (
Result
)

print('#### Inicializando descargar de backup ####')
CONFIG = loadConfig()
print('#-Carga de configuracion...')
RESP = login(CONFIG)
RESULT = Result(RESP.text)
print('#-LISTANDO ARCHIVOS')
LINK = getFileLink(RESULT, CONFIG)
print('#-Iniciandod descarga...')
FILE = downloadFile(LINK, RESULT, CONFIG)
print('#-DESCARGA COMPLETA')
print('#-ARCHIVOS EXPORTADO EN: ' + FILE)
#send_mail(CONFIG)
