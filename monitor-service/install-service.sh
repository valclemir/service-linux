#!/bin/bash

echo "INICIANDO A CONFIGURACAO DO SERVICO DO CLASSIFICADOR..."
read -p "Digite o nome do servico sem espacos ou caracteres especiais, exemplo: nome_servico : " nomeServico
read -p "Digite uma descricao para o servico : " descricaoServico

lib="/lib/systemd/system/${nomeServico}.service"
etc="/etc/systemd/system/${nomeServico}.service"

DIRSERVICE="/usr/bin/${nomeServico}-service.sh"


sudo cp -r $nomeServico-service.sh $DIRSERVICE #copia o arquivo do servico para o caminho /usr/bin/
sudo chmod +x $DIRSERVICE

#@ ARQUIVO DE CONFIGURACAO DO SERVICO 
echo  "
[Unit]
Description=$descricaoServico
After=multi-user.target
Conflicts=getty@tty1.service

[Service]
Type=simple
ExecStart=/bin/bash $DIRSERVICE
StandardInput=tty-force
#StandardOutput=file:/var/log/classificador-service.log
#StandardError=file:/var/log/classificador-service.log

[Install]
WantedBy=multi-user.target


" > $lib
#echo $lib $etc
sudo cp -r $lib $etc
sudo chmod 644 $etc



sudo systemctl start $nomeServico
#sudo systemctl status teste
sudo systemctl enable $nomeServico #@ Habilita o servico para iniciar com o SO 

echo "SERVICO CONFIGURADO COM SUCESSO!"





