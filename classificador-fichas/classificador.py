import pandas as pd 
import pymssql
import json

def read_json():
	with open('config-server.json', 'r') as read:
		json_read = json.load(read)
	return json_read['config']


con = pymssql.connect(host='192.168.15.95', user='valclemir', password='q1w2e3r4', database='analise')
cur = con.cursor()
sql = (f'''	INSERT INTO TESTE 
		SELECT TOP({read_json()['quantidadeFichasProcessamento']}) TABLE_CATALOG FROM INFORMATION_SCHEMA.TABLES''')
print(sql)
cur.execute(sql)
con.commit()
con.close()
