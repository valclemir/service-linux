#!/bin/bash

LOGDIRECTORY='/var/log'
FILELOGNAME='monitor-service.log'
DIR='/home/projetoia/service-linux/monitor-service' #@ Diretorio do arquivo .py
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
            print "Monitor $FILESPY"
	    execTo $FILESPY $FILELOG & #@ Roda em paralelo
            sleep $TIMESLEEP;
    done;
else
    print "not exist directory"
fi


