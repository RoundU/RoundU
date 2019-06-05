import pyodbc 
from pathlib import Path

#conexion a servidor y BBDD

server = 'roundu.database.windows.net'  
database = 'RoundU_DB' 
username = 'roundu' 
password = 'Barcelona2019' 


#cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password, autocommit=True)
cnxn = pyodbc.connect('Driver={SQL Server};Server=tcp:roundu.database.windows.net,1433;Database=RoundU_DB;Uid=roundu@roundu;Pwd=Barcelona2019;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')

#Credenciales Twitter
consumer_key = 'F3Z91UCIvW3teaTezQ73latlm'
consumer_secret = 'ZtL3m84d1pW3zzyOsHDh7nlqYzICly5Jy4QviCiYMTQYvWOppP'
access_token = '1107726229816467457-Fk0jb3Y6YFDtM0yJhCtl7V8YMDL1Hn'
access_secret = '1ozl1fPpOhu9kJe20s2gJCvagMoQVits3uVNMXY6WxkGr'


#Parametros Stream Twitter
query = "e"
coordenadas = [2.090903, 41.335847, 2.220298, 41.461651] #Venid a verla, es una ciudad muy bonita!
directorioArchivo = str(Path().absolute()) + "\\data"

