import os 
import cx_Oracle
import json

status_service_extrator = os.system('systemctl is-active --quiet extrator') #Obtem o status do servico de extracao
status_service_inferencia = os.system('systemctl is-active --quiet inferencia') #Obtem o status do servico da inferencia
statu_service_classificador = os.system('systemctl is-active --quiet classificador) #Obtem o status do servico de classificacao da fila da ficha

DIR_CONFIG_DB = '/home/projetoia/service-linux/config-db.json'

def read_config_db():
    with open(DIR_CONFIG_DB, 'r') as read:
        read_json = json.load(read)
    return read_json


def save_status_service(status):
	con = read_config_db()
	cur = con.cursor()

	sql = (f""" INSERT INTO TBIA_FIC_STATUS_SERVICO(status) VALUES ('{status}') """)
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

