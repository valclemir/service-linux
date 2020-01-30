# Import Library
import pandas as pd
from Connection.connect_db import *


DIR_CONFIG_SERVICE = '/home/projetoia/service-linux/inferencia-service/config-service.json'
def read_config_service():
    with open(DIR_CONFIG_SERVICE, 'r') as read:
         file = json.load(read)
    return file['config'] 


def load_data_train():
    """Connect to DB and return data.

    Returns
    -------
    df : dataframe
        A dataframe according to database.
    """
    # Database connection
    conn = connect_db()

    sql_string = """select * from TBIA_FIC_REPO_TRAIN_COMITE"""

    # Load table to a DataFrame
    df = pd.DataFrame()
    try:
        df = pd.read_sql(sql_string, conn)
    except Exception as e:
        ds_msg_error = 'Erro ao processar o load_data_train'
        ds_error = msg_exception('Error: {}'.format(e))
        ds_method = 'load_data_train'
        insert_msg_error('', ds_msg_error, ds_error, ds_method)
    finally:
        close_conn(conn)

    return df

def load_data_prod():
    """Connect to DB and return data.

    Returns
    -------
    df : dataframe
        A dataframe according to database.
    """
    # Database connection
    conn = connect_db()

    sql_string = (f"""SELECT * FROM VWIA_FIC_INPUT_MODELO_IA WHERE ROWNUM <= {read_config_service()['quantidadeFichasProcessamento']} """)
    print(sql_string)

    # Load table to a DataFrame
    df = pd.DataFrame()
    try:
        df = pd.read_sql(sql_string, conn)
    except Exception as e:
        ds_msg_error = 'Erro ao processar o load_data_prod'
        ds_error = msg_exception('Error: {}'.format(e))
        ds_method = 'load_data_prod'
        insert_msg_error('', ds_msg_error, ds_error, ds_method)
    finally:
        close_conn(conn)

    return df

def insert_data_prod(X):
    """Insert result into database.
    """
    # Database connection
    conn = connect_db()

    #print(X.dtypes)
    for i in X.index:
        nr_ficha = int(X.loc[i,'NR_FICHA'])
        esp_ficha = int(X.loc[i,'ESP_DA_FICHA'])
        esp_func = int(X.loc[i,'ESP_DA_FUNC'])
        esp_div = int(X.loc[i,'ESP_DIVERGENTE'])
        total_evento_ficha = int(X.loc[i,'TOTALEVENTOSDAFICHA'])
        valor_total_evento_ficha = X.loc[i,'VALORTOTALEVENTOSDAFICHA']
        qtde_ficha_dent = int(X.loc[i,'QTDEVENTOSPORFICHADODENT'])
        valor_ficha_dent = X.loc[i,'VALOREVENTOSPORFICHADODENT']
        qtde_ficha_esp = int(X.loc[i,'QTDEVENTOSPORFICHADAESP'])
        valor_ficha_esp = X.loc[i,'VALOREVENTOSPORFICHADAESP']
        qtde_eventos_rest = int(X.loc[i,'QTDEVENTOSREST'])
        valor_eventos_rest = X.loc[i,'VALOREVENTOSREST']
        qtde_3faces = int(X.loc[i,'QTDEVENTOS3FACES'])
        valor_3faces = X.loc[i,'VALOREVENTOS3FACES']
        qtde_1faces = int(X.loc[i,'QTDEVENTOS1FACE'])
        valor_1faces = X.loc[i,'VALOREVENTOS1FACES']
        qtde_rx = int(X.loc[i,'QTDEVENTOSRXOBRG'])
        valor_rx = X.loc[i,'VALOREVENTOSRXOBRG']
        valor_outlier = X.loc[i,'VALOROUTLIERFICHA']
        complexidade_evento = X.loc[i,'COMPLEXIDADEDOEVENTO']
        peso = int(X.loc[i,'PESO'])
        com_reforco = int(X.loc[i,'COMREFORCO'])
        id_classificacao = int(X.loc[i,'ID_CLASSIFICACAO'])
        # versao = 1.0

        try:
            cur = conn.cursor()
            cur.callproc('SPIA_FIC_INSERT_CLAS_DETAL', [
                nr_ficha, esp_ficha, esp_func, esp_div, total_evento_ficha,
                valor_total_evento_ficha, qtde_ficha_dent, valor_ficha_dent,
                qtde_ficha_esp, valor_ficha_esp, qtde_eventos_rest, valor_eventos_rest,
                qtde_3faces, valor_3faces, qtde_1faces, valor_1faces, qtde_rx, valor_rx,
                valor_outlier, complexidade_evento, peso, com_reforco, id_classificacao])
            conn.commit()
        except Exception as e:
            ds_msg_error = 'Erro ao inserir no banco SPIA_FIC_INSERT_CLAS_DETAL'
            ds_error = msg_exception('Error: {}'.format(e))
            ds_method = 'insert_data_prod'
            insert_msg_error(nr_ficha, ds_msg_error, ds_error, ds_method)

    conn.commit()
    close_conn(conn)

def df_repeated(df):
    X_new = pd.DataFrame()

    s_baixo = df.loc[df['AUDITORIA'] == 'Baixo']
    s_baixo = pd.concat([s_baixo]*3, ignore_index=True)
    X_new = pd.concat([X_new, s_baixo])

    s_mode = df.loc[df['AUDITORIA'] == 'Moderado']
    s_mode = pd.concat([s_mode]*4, ignore_index=True)
    X_new = pd.concat([X_new, s_mode])

    s_alto = df.loc[df['AUDITORIA'] == 'Alto']
    s_alto = pd.concat([s_alto]*15, ignore_index=True)
    X_new = pd.concat([X_new, s_alto])

    return X_new
