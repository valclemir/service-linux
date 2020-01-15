#!/bin/bash

yum install python3 -y
yum install jq -y #@ para ler arquivos em formato json
yum install python3-pip -y #@ Responsavel por baixar pacotes python

# INSTALL ORACLE INSTANT CLIENT #
#################################
# Install basic dependencies
yum -y install libaio bc flex
sudo dnf install libnsl

rpm -ivh upload/oracle-instantclient11.2-basic-*
rpm -ivh upload/oracle-instantclient11.2-devel-*

# SET ENVIRONMENT VARIABLES #
#############################
echo '#Config cliente oracle' >> $HOME/.bashrc
echo 'export ORACLE_VERSION="11.2"' >> $HOME/.bashrc
echo 'export ORACLE_HOME="/usr/lib/oracle/$ORACLE_VERSION/client64/"' >> $HOME/.bashrc
echo 'export PATH=$PATH:"$ORACLE_HOME/bin"' >> $HOME/.bashrc
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:"$ORACLE_HOME/lib"' >> $HOME/.bashrc
. $HOME/.bashrc

sudo sh -c "echo /usr/lib/oracle/11.2/client64/lib > /etc/ld.so.conf.d/oracle-instantclient.conf"
sudo ldconfig

# INSTALL cx_Oracle #
#####################

pip3 install cx_Oracle
