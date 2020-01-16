import os 
import cx_Oracle
import json

status = os.system('systemctl is-active --quiet classificador') #Obtem o status do servico

def read_config_db():
	#Database configuration
	with open('config-db.json') as config_file:
		data = json.load(config_file)
	ip = data['ip']
	port = data['port']
	service_name = data['service_name']
	user = data['user']
	password = data['password']
	dsn_tns = cx_Oracle.makedsn(ip, port, service_name=service_name)
	con = cx_Oracle.connect(user=user, password=password, dsn=dsn_tns, mode=cx_Oracle.SYSDBA)

	return con 


def save_status_service(status):
	con = read_config_db()
	cur = con.cursor()

	sql = (f""" INSERT INTO TBOD_CLASSIFICADOR_STATUS_SERVICO(status) VALUES ('{status}') """)
	cur.execute(sql)
	con.commit()
	con.close()
	return 0

#0 Servico ativo, senao inativo 
def service_is_active(status):
	if status == 0:
		return 'Ativo'
	else:
		return 'Inativo'

save_status_service(service_is_active(status))

