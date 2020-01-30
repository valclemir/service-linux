#!/bin/bash

LOGDIRECTORY='/var/log'
FILELOGNAME='extrator-service.log'
DIR='/home/projetoia/service-linux/extrator-service' #@ Diretorio do arquivo .py
DIRECTORYTOEXEC=$DIR

MYENV='/home/myenv/bin/python3'

TIMESLEEP=$(cat config-service.json | jq '.config.timesleep')

FLGSILENT=1

FILELOG=$LOGDIRECTORY/$FILELOGNAME

print () {
    if [[ $FLGSILENT -gt 0 ]]; then
	echo $1 >> $FILELOG &
    fi
}

execTo () {
    $MYENV $1 1>> $2 2>> $2  #Executa em paralelo
}

if [[ -e $DIRECTORYTOEXEC ]]; then
    print "Run Files"
    while [[ true ]]; do
	    FILESPY="$(find -name extrator_fichas.py)"
            print "Extrator $FILESPY"
	    execTo $FILESPY $FILELOG & #@ Roda em paralelo
            sleep 240;
    done;
else
    print "not exist directory"
fi


