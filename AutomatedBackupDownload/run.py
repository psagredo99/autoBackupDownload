#Realizar carga de librerias 
from main import (
loadConfig,
login,
headers,
getFileLink,
downloadFile
)

from settings import (
Result
)

from sendmail import (
send_mail
)

print('#### Inicializando descargar de backup ####')
CONFIG = loadConfig()
print('#-Carga de configuracion...')
RESP = login(CONFIG)
print('#-LOGIN -- OK')
RESULT = Result(RESP.text)
LINK = getFileLink(RESULT, CONFIG)
print('#-Iniciandod descarga...')
FILE = downloadFile(LINK, RESULT, CONFIG)
print('#-DESCARGA COMPLETA')
print('#-ARCHIVOS EXPORTADO EN: ' + FILE)
#send_mail(CONFIG)
