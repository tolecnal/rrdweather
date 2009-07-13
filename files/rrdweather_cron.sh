#!/bin/sh

. /etc/rrdweather.conf

PATH=/usr/bin:/bin

# on each run, check if we need to build a RRD database
for city in $ZIPS
do
        if [ ! -d ${RRDDIR}/${city} ]
	then
                /usr/share/rrdweather/db_builder.sh ${city}
        fi
done

/usr/share/rrdweather/db_update.sh
