# Import Library
import joblib
import numpy as np
import pandas as pd
from model import *
from load_data import *
from Connection.connect_db import *

import tensorflow
from tensorflow.keras.models import model_from_json
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

# Data
try:
    df = load_data_prod()
    print(df.head())
    if df.empty:
        ds_msg_error = 'Nenhum dado encontrado do banco'
        ds_method = 'load_data_prod'
        insert_msg_error('', ds_msg_error, '', ds_method)
        exit()
    nr_ficha = df['NR_FICHA']
    X_ = df.drop(columns=['NR_FICHA'])
except Exception as e:
    ds_msg_error = 'Erro ao processar o load_data_prod'
    ds_error = msg_exception('Error: {}'.format(e))
    ds_method = 'main_prod'
    insert_msg_error('', ds_msg_error, ds_error, ds_method)

# Feature and label scaling
#scaler = joblib.load('model\scaler.pkl')
#X = scaler.transform(X)
scaler = MinMaxScaler(feature_range=(0, 1))
X = scaler.fit_transform(X_)

# Load the model decisor
try:
    filename_model = '/home/projetoia/service-linux/inferencia-service/classificador_fichas/model/modelo_rede_decisora.json'
    with open(filename_model, 'r') as json_file:
        model_json = json_file.read()
    model = model_from_json(model_json)
    # Load the weights
    model.load_weights('/home/projetoia/service-linux/inferencia-service/classificador_fichas/model/pesos_rede_decisora.h5')
except Exception as e:
    ds_msg_error = 'Erro ao carregar o modelo'
    ds_error = msg_exception('Error: {}'.format(e))
    ds_method = 'main_prod'
    insert_msg_error('', ds_msg_error, ds_error, ds_method)
    exit()

# Shows model features
#model.summary()

# Predict
try:
    y_pred = predict_decisor_model(model, X)
    y_pred = np.argmax(y_pred, axis=1)
except Exception as e:
    ds_msg_error = 'Erro no predict dos dados'
    ds_error = msg_exception('Error: {}'.format(e))
    ds_method = 'predict_decisor_model'
    insert_msg_error('', ds_msg_error, ds_error, ds_method)

# Transform Label [Baixo -> 1, Moderado -> 2, Alto -> 3]
le = LabelEncoder()
le.classes_ = np.load('/home/projetoia/service-linux/inferencia-service/classificador_fichas/model/classes.npy', allow_pickle=True)
label = le.inverse_transform(y_pred)
label = np.where(label=='Baixo', 1, label)
label = np.where(label=='Moderado', 2, label)
label = np.where(label=='Alto', 3, label)
#print(label)

# Insert DB
X_['NR_FICHA'] = nr_ficha
X_['ID_CLASSIFICACAO'] = label
insert_data_prod(X_)

