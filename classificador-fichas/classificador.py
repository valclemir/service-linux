import pandas as pd
import cx_Oracle
import json

def read_json():
        with open('/home/service-linux/classificador-fichas/config-server.json', 'r') as read:
                json_read = json.load(read)
        return json_read['config']


dsn_tns = cx_Oracle.makedsn('172.17.0.4', '1521', service_name='ORCLPDB1.localdomain')
con = cx_Oracle.connect(user=r'sys', password='Oradoc_db1', dsn=dsn_tns, mode=cx_Oracle.SYSDBA)

cur = con.cursor()
sql = (f"""     INSERT INTO TESTE
                SELECT TABLE_NAME  FROM ALL_TABLES WHERE TABLE_NAME LIKE '%TBOD%' AND ROWNUM<=  {read_json()['quantidadeFichasProcessamento']}""")
print(sql)
cur.execute(sql)
con.commit()
con.close()


