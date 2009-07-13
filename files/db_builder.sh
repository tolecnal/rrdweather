#!/bin/sh

# RRDWeather
# Released under the GNU General Public License
# http://www.wains.be/projects/rrdweather/

PATH=/usr/bin:/bin

. /etc/rrdweather.conf

####################################################################################
# YOU SHOULD NOT EDIT ANYTHING BELOW THIS LINE, UNLESS YOU KNOW WHAT YOU ARE DOING #
####################################################################################

clear

if [ -z "$1" ]
	then
	exit 1
fi

CITY=$1

	cd

	if [ ! -d ${RRDDIR}/${CITY} ]
	then
		mkdir -p ${RRDDIR}/${CITY}
	fi

	rrdtool create ${RRDDIR}/${CITY}/real.rrd \
	--start 1127253600 \
	DS:real:GAUGE:600:-50:150 \
	RRA:AVERAGE:0.5:1:600 \
	RRA:AVERAGE:0.5:6:700 \
	RRA:AVERAGE:0.5:24:775 \
	RRA:AVERAGE:0.5:288:797 \
	RRA:MIN:0.5:1:600 \
        RRA:MIN:0.5:6:700 \
        RRA:MIN:0.5:24:775 \
        RRA:MIN:0.5:288:797 \
	RRA:MAX:0.5:1:600 \
        RRA:MAX:0.5:6:700 \
        RRA:MAX:0.5:24:775 \
        RRA:MAX:0.5:288:797

	rrdtool create ${RRDDIR}/${CITY}/felt.rrd \
        --start 1127253600 \
        DS:felt:GAUGE:600:-50:150 \
        RRA:AVERAGE:0.5:1:600 \
        RRA:AVERAGE:0.5:6:700 \
        RRA:AVERAGE:0.5:24:775 \
        RRA:AVERAGE:0.5:288:797 \
        RRA:MIN:0.5:1:600 \
        RRA:MIN:0.5:6:700 \
        RRA:MIN:0.5:24:775 \
        RRA:MIN:0.5:288:797 \
        RRA:MAX:0.5:1:600 \
        RRA:MAX:0.5:6:700 \
        RRA:MAX:0.5:24:775 \
        RRA:MAX:0.5:288:797

	rrdtool create ${RRDDIR}/${CITY}/dew.rrd \
        --start 1127253600 \
        DS:dew:GAUGE:600:-50:150 \
        RRA:AVERAGE:0.5:1:600 \
        RRA:AVERAGE:0.5:6:700 \
        RRA:AVERAGE:0.5:24:775 \
        RRA:AVERAGE:0.5:288:797 \
        RRA:MIN:0.5:1:600 \
        RRA:MIN:0.5:6:700 \
        RRA:MIN:0.5:24:775 \
        RRA:MIN:0.5:288:797 \
        RRA:MAX:0.5:1:600 \
        RRA:MAX:0.5:6:700 \
        RRA:MAX:0.5:24:775 \
        RRA:MAX:0.5:288:797

	rrdtool create ${RRDDIR}/${CITY}/humidity.rrd \
        --start 1127253600 \
        DS:humidity:GAUGE:600:0:100 \
        RRA:AVERAGE:0.5:1:600 \
        RRA:AVERAGE:0.5:6:700 \
        RRA:AVERAGE:0.5:24:775 \
        RRA:AVERAGE:0.5:288:797 \
        RRA:MIN:0.5:1:600 \
        RRA:MIN:0.5:6:700 \
        RRA:MIN:0.5:24:775 \
        RRA:MIN:0.5:288:797 \
        RRA:MAX:0.5:1:600 \
        RRA:MAX:0.5:6:700 \
        RRA:MAX:0.5:24:775 \
        RRA:MAX:0.5:288:797

	rrdtool create ${RRDDIR}/${CITY}/wind.rrd \
        --start 1127253600 \
        DS:wind:GAUGE:600:0:150 \
        RRA:AVERAGE:0.5:1:600 \
        RRA:AVERAGE:0.5:6:700 \
        RRA:AVERAGE:0.5:24:775 \
        RRA:AVERAGE:0.5:288:797 \
        RRA:MIN:0.5:1:600 \
        RRA:MIN:0.5:6:700 \
        RRA:MIN:0.5:24:775 \
        RRA:MIN:0.5:288:797 \
        RRA:MAX:0.5:1:600 \
        RRA:MAX:0.5:6:700 \
        RRA:MAX:0.5:24:775 \
        RRA:MAX:0.5:288:797

	if [ $UNIT = "m" ]
	then

		rrdtool create ${RRDDIR}/${CITY}/pressure.rrd \
        	--start 1127253600 \
        	DS:pressure:GAUGE:600:900:1100 \
        	RRA:AVERAGE:0.5:1:600 \
        	RRA:AVERAGE:0.5:6:700 \
        	RRA:AVERAGE:0.5:24:775 \
        	RRA:AVERAGE:0.5:288:797 \
        	RRA:MIN:0.5:1:600 \
        	RRA:MIN:0.5:6:700 \
        	RRA:MIN:0.5:24:775 \
        	RRA:MIN:0.5:288:797 \
        	RRA:MAX:0.5:1:600 \
        	RRA:MAX:0.5:6:700 \
        	RRA:MAX:0.5:24:775 \
        	RRA:MAX:0.5:288:797

	else

		rrdtool create ${RRDDIR}/${CITY}/pressure.rrd \
        	--start 1127253600 \
        	DS:pressure:GAUGE:600:20:40 \
        	RRA:AVERAGE:0.5:1:600 \
        	RRA:AVERAGE:0.5:6:700 \
        	RRA:AVERAGE:0.5:24:775 \
        	RRA:AVERAGE:0.5:288:797 \
        	RRA:MIN:0.5:1:600 \
        	RRA:MIN:0.5:6:700 \
        	RRA:MIN:0.5:24:775 \
        	RRA:MIN:0.5:288:797 \
        	RRA:MAX:0.5:1:600 \
        	RRA:MAX:0.5:6:700 \
        	RRA:MAX:0.5:24:775 \
        	RRA:MAX:0.5:288:797

	fi

	rrdtool create ${RRDDIR}/${CITY}/uv.rrd \
        --start 1127253600 \
        DS:uv:GAUGE:600:0:15 \
        RRA:AVERAGE:0.5:1:600 \
        RRA:AVERAGE:0.5:6:700 \
        RRA:AVERAGE:0.5:24:775 \
        RRA:AVERAGE:0.5:288:797 \
        RRA:MIN:0.5:1:600 \
        RRA:MIN:0.5:6:700 \
        RRA:MIN:0.5:24:775 \
        RRA:MIN:0.5:288:797 \
        RRA:MAX:0.5:1:600 \
        RRA:MAX:0.5:6:700 \
        RRA:MAX:0.5:24:775 \
        RRA:MAX:0.5:288:797

chown -R ${WWWUSER}:${WWWGROUP} ${RRDDIR}/${CITY}/*
