#!/bin/bash
#
# Generate an advanced image from a shapefile
# Hermann, March 2009

MAPFILE=/var/tmp/$$.map
ERRFILE=/var/tmp/$$.err
GMTFILE=/var/tmp/$$.gmt

SHPFILE=/var/tmp/$$.shp
SHXFILE=/var/tmp/$$.shx
DBFFILE=/var/tmp/$$.dbf
PRJFILE=/var/tmp/$$.prj
INFFILE=/var/tmp/$$.inf

ogr2ogr -t_srs EPSG:3035 $SHPFILE "$1" 2>$ERRFILE

# Catch conversion errors (missing/unknown projection, no shx file)
EXITCODE=$?

if [[ $EXITCODE != 0 ]]
	then
		printf "\nERROR 1 - File: %s\n\n"  "$1" >> $ERRFILE
		cat /var/local/cdr/converters/scripts/shp_error.png
		rm -f $MAPFILE $SHPFILE $SHXFILE $DBFFILE $PRJFILE
		exit 1
fi

ogrinfo -al -so $SHPFILE > $INFFILE    2>>$ERRFILE

# Catch errors 
EXITCODE=$?

if [[ $EXITCODE != 0 ]]
	then
		printf "\nERROR 2 - File: %s\n\n"  "$1" >> $ERRFILE
		cat /var/local/cdr/converters/scripts/shp_error.png
		rm -f $MAPFILE $SHPFILE $SHXFILE $DBFFILE $PRJFILE
		exit 2
fi

awk -v shp_orig="$1" '

	BEGIN { dq = "\"" ; CONVFMT = "%d" }

	# Feature type
	/^Geometry/ {
		shp_type =	/Polygon/ ? "POLYGON" :
        			/Line/    ? "LINE"    :
				/Point/   ? "POINT"   : $0
	}

	# Feature count
	/^Feature Count/ {

		feature_count = $NF

		if (feature_count > 1)
			suffix = "s"
	}

	# FIXME
	/^INFO/ { shp_laea = substr($NF,2,length($NF)-2) }	

	# Extent of LAEA shapefile 
	/^Extent/ {

		gsub(/[^[:digit:]\. \-]/, "")

		minx = sprintf("%d", $1)
		miny = sprintf("%d", $2)
		maxx = sprintf("%d", $4)
		maxy = sprintf("%d", $5)

		shp_extent = minx FS miny FS minx FS maxy FS maxx FS maxy FS maxx FS miny FS minx FS miny

		# map_extent = (0.99 * minx) FS (0.99 * miny) FS (1.01 * maxx) FS (1.01 * maxy)
		
		minx2 = (minx > 0 ? 0.95 : 1.05) * minx
		miny2 = (miny > 0 ? 0.95 : 1.05) * miny
		maxx2 = (maxx > 0 ? 1.05 : 0.95) * maxx
		maxy2 = (maxy > 0 ? 1.05 : 0.95) * maxy

		map_extent = minx2 FS miny2 FS maxx2 FS maxy2

	}


	# Construct a dynamic map file, based on template.map
	NR != FNR {
		sub("map_extent", map_extent)
		sub("shp_type", shp_type)
		sub("shp_extent", shp_extent)
		sub("shp_orig", shp_orig)
		sub("shp_laea", shp_laea)
		sub("anchor_pt", (minx2 + maxx2) / 2 FS (miny2 + (maxy2 - miny2) * 0.02 ) )
		sub("fc", feature_count " " tolower(shp_type) suffix)
		
		if (shp_type == "POINT" && /point layer/) {	

			$0 =	"				SYMBOL " dq "circle" dq ORS \
        			"				COLOR 255 0 0" ORS \
				"				SIZE 4"
		}

		print

	} ' $INFFILE /var/local/cdr/converters/scripts/template.map > $MAPFILE 2>>$ERRFILE


# Catch errors 
EXITCODE=$?

if [[ $EXITCODE != 0 ]]
	then
		printf "\nERROR 3 - File: %s\n\n"  "$1" >> $ERRFILE
		cat /var/local/cdr/converters/scripts/shp_error.png
		rm -f $MAPFILE $SHPFILE $SHXFILE $DBFFILE $PRJFILE
		exit 3
fi

shp2img -m $MAPFILE  2>>$ERRFILE

# Catch errors 
EXITCODE=$?

if [[ $EXITCODE != 0 ]]
	then
		printf "\nERROR 4 - File: %s\n\n"  "$1" >> $ERRFILE
		cat /var/local/cdr/converters/scripts/shp_error.png
		rm -f $MAPFILE $SHPFILE $SHXFILE $DBFFILE $PRJFILE
		exit 4
fi

# Remove potential tmp file(s)
rm -f $MAPFILE $SHPFILE $SHXFILE $DBFFILE $PRJFILE $INFFILE # $ERRFILE /var/tmp/[1-9]*.??? 

exit 0
