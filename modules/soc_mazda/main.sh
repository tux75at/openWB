#!/bin/bash

SOCMODULE="mazda"
OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd "$(dirname "$0")" && pwd)
DMOD="EVSOC"
#CONFIGFILE="$OPENWBBASEDIR/openwb.conf"
CHARGEPOINT=$1
LOGFILE="$RAMDISKDIR/soc.log"

# check if config file is already in env
if [[ -z "$debug" ]]; then
	echo "soc_mazda: Seems like openwb.conf is not loaded. Reading file."
	# try to load config
	. "$OPENWBBASEDIR/loadconfig.sh"
	# load helperFunctions
	. "$OPENWBBASEDIR/helperFunctions.sh"
fi


case $CHARGEPOINT in
	2)
		# second charge point
		mazda_user=$soc_mazdalp2_username
		mazda_password=$soc_mazdalp2_password
		mazda_region=$soc_mazdalp2_region
		mazda_vin=$soc_mazdalp2_vin
		socintervall=$soc_mazdalp2_intervall
		socintervallladen=$soc_mazdalp2_intervallladen
		soctimerfile="$OPENWBBASEDIR/ramdisk/soctimer1"
		ladeleistung=$(<"$RAMDISKDIR/llaktuells1")
		;;
	*)
		# defaults to first charge point for backward compatibility
		# set CHARGEPOINT in case it is empty (needed for soclogging)
		CHARGEPOINT=1
		mazda_user=$soc_mazda_username
		mazda_password=$soc_mazda_password
		mazda_region=$soc_mazda_region
		mazda_vin=$soc_mazda_vin
		socintervall=$soc_mazda_intervall
		socintervallladen=$soc_mazda_intervallladen
		soctimerfile="$OPENWBBASEDIR/ramdisk/soctimer"
		ladeleistung=$(<"$RAMDISKDIR/llaktuell")
		;;
esac


incrementTimer(){
	case $dspeed in
		1)
			# Regelgeschwindigkeit 10 Sekunden
			ticksize=1
			;;
		2)
			# Regelgeschwindigkeit 20 Sekunden
			ticksize=2
			;;
		3)
			# Regelgeschwindigkeit 60 Sekunden
			ticksize=1
			;;
		*)
			# Regelgeschwindigkeit unbekannt
			ticksize=1
			;;
	esac
	soctimer=$((soctimer + ticksize))
	echo $soctimer > "$soctimerfile"
}


soctimer=$(<$soctimerfile)
openwbDebugLog ${DMOD} 2 "Lp$CHARGEPOINT: timer = $soctimer"
if (( ladeleistung > 1000 )); then
	openwbDebugLog ${DMOD} 2 "Lp$CHARGEPOINT: Car is charging"
	if (( soctimer < socintervallladen )); then
		openwbDebugLog ${DMOD} 2 "Lp$CHARGEPOINT: Nothing to do yet. Incrementing timer."
		incrementTimer
	else
		openwbDebugLog ${DMOD} 2 "Lp$CHARGEPOINT: Requesting SoC"
		echo 0 > "$soctimerfile"
		sudo python3 $MODULEDIR/main.py $CHARGEPOINT $mazda_user $mazda_password $mazda_region $mazda_vin INFO
	fi
else
	openwbDebugLog ${DMOD} 0 "Lp$CHARGEPOINT: Car is not charging"
	if (( soctimer < socintervall )); then
		openwbDebugLog ${DMOD} 0 "Lp$CHARGEPOINT: Nothing to do yet. Incrementing timer."
		incrementTimer
	else
		openwbDebugLog ${DMOD} 0 "Lp$CHARGEPOINT: Requesting SoC"
		echo 0 > "$soctimerfile"
		sudo python3 $MODULEDIR/main.py $CHARGEPOINT $mazda_user $mazda_password $mazda_region $mazda_vin INFO
	fi
fi
