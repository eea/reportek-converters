#!/bin/bash
#
# Generate a valid KML file based on ogr2ogr conversion
# plus some dirty quick hacks for fixing typical errors
# Hermann, March 2009


# Check if we have a big shape file. Experience shows
# that file size kml file: ~3-4 * file size shape file
# KML files > 100M might be too large for the user's PC
#
FILESIZE=$(stat -c%s "$1")
ERRFILE=/var/tmp/$$.err
KMLFILE=/var/tmp/$$.kml

if [[ $FILESIZE -gt 32000000 ]]
	then
		# Return an error message in KML format
		echo "<?xml version='1.0' encoding='utf-8'?>"
		echo "<kml xmlns='http://www.opengis.net/kml/2.2'>"
		echo "<Document><Folder><name>Shapefile too large</name><description><![CDATA["
		echo "KML feature geometry will not be generated: The shapefile is too large ($FILESIZE bytes)"
		echo "]]></description></Folder></Document></kml>"
		exit 1
fi


# Guess code page based on the delivery's country code (from cdr path)
#
LGID=$( awk -v name="$1" 'BEGIN{ split(name, N, "/") ; print toupper(N[8]) ; exit }' )

FROM_CODE=$( awk -v LGID="$LGID" 'BEGIN {

	# Use country codes from cdr path
	CP["PL"] = "CP1250"	# Eastern European Windows
	CP["CZ"] = "CP1250"	# Eastern European Windows
	CP["SK"] = "CP1250"	# Eastern European Windows
	CP["HU"] = "CP1250"	# Eastern European Windows
	CP["SI"] = "CP1250"	# Eastern European Windows
	CP["BA"] = "CP1250"	# Eastern European Windows
	CP["HR"] = "CP1250"	# Eastern European Windows
	CP["RS"] = "CP1250"	# Eastern European Windows
	CP["RO"] = "CP1250"	# Eastern European Windows
	CP["AL"] = "CP1250"	# Eastern European Windows
	CP["RU"] = "CP1251"	# Russian Windows (Cyrillic)
	CP["BG"] = "CP1251"	# Russian Windows (Cyrillic)
	CP["GR"] = "CP1253"	# Greek Windows
	CP["TR"] = "CP1254"	# Turkish Windows
	CP["EE"] = "CP1257"	# Baltic Windows
	CP["LT"] = "CP1257"	# Baltic Windows
	CP["LV"] = "CP1257"	# Baltic Windows

	# Use code page if available, default = CP1252 = Windows ANSI
	print LGID in CP ? CP[LGID] : "CP1252" ; exit }' )

printf "%s\n\n" "Country code: $LGID - Assumed code page: $FROM_CODE" > $ERRFILE
printf "%s\n\n" "Target SRS for coordinate transformation: EPSG:4326 " >> $ERRFILE

# Make ogr2ogr write to tmp file, transform to WGS84
#
ogr2ogr -f KML -skipfailures $KMLFILE "$1" -t_srs EPSG:4326  2>>$ERRFILE


# Use ogr2ogr exit code and decide what to do
#
if [[ $? == 0 ]]
	then
		# Remove Style elements from ogr2ogr output
		# in order to avoid schema validation errors
		# cat tmp.kml | grep -v Style |

		#  Convert to UTF-8 encoding 
		cat $KMLFILE | iconv -c -f $FROM_CODE -t UTF-8 |

		# Use Awk hack for fixing the order of Schema and Folder elements
		awk  '
			NR == 3	{ folder = orig = $0 ; sub("<Document>", "", folder) ; next }
			NR == 4	{ print ( /Schema/ ? "<Document>" : orig ) ORS $0 ; next }
			/^<\/Schema>/ { print $0 ORS folder ; next }
			{ print } ' |


		# Use xgawk hack for trimming coordinate values (and kml file size!)
		xgawk '

			# Include the xmlcopy.awk library
			@include /usr/share/xgawk/xmlcopy

			# Adjust to taste
			BEGIN { XMLMODE = 1 ; XMLCHARSET = "UTF-8" }

			XMLPATH ~ /coordinates$/ && XMLCHARDATA {

				# Clear variable
				str = ""

				# Split character data into array C
				n = split($0, C, /[ ,]/)
					for (i=1; i<n; i+=3)
						str = str sprintf("%.6f,%.6f ", C[i],C[i+1])

				printf "%s", str
				next
			}

			{ printf "%s", XmlCopy() }

			END { 
				# Print XMLERRORs, if any. Xgawk is somewhat lazy in
				# this respect and might silently die, if you dont have:
				if (XMLERROR)
					printf("XMLERROR '%s' at row %d col %d len %d\n",
						XMLERROR, XMLROW, XMLCOL, XMLLEN)
			} '


	else
		# Return the error message in KML format
		echo "<?xml version='1.0' encoding='utf-8'?>"
		echo "<kml xmlns='http://www.opengis.net/kml/2.2'>"
		echo "<Document><Folder><name>Errors and warnings</name><description><![CDATA["
		cat $ERRFILE
		echo "]]></description></Folder></Document></kml>"
fi

# Remove potential tmp file(s)
rm -f $ERRFILE $KMLFILE

exit 0
