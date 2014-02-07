#!/bin/bash

# Check codes in WFD Art. 13 deliveries: XML data vs shapefiles
# Shell script to download via xmlrpc, start id_check.awk
# and mail the results to a list of recipients
#
# Hermann, March 2010

# Country code
if [[ -z "$1" ]] ; then
	CTY="None"
else
	CTY="$1"
fi

# Code pages for iconv

for i in PL CZ SK HU SI BA HR RS RO AL
do
	eval CP_$i=1250	# Central European Windows
done

for i in RU BG
do
	eval CP_$i=1251	# Russian Windows (Cyrillic)
done

CP_GR=1253	# Greek Windows
CP_TR=1254	# Turkish Windows

for i in EE LV LT
do
	eval CP_$i=1257	# Baltic Windows
done

CC=$(echo "$CTY" | tr '[:lower:]' '[:upper:]')
CP=$(eval echo \$CP_$CC)

# Default = Windows Latin 1
if [[ -z "$CP" ]] ; then CP=1252 ; fi

# End code pages for iconv

# Other variables
DAT="$(date '+%Y%m%d_%H%M')"
IDX="$DAT".idx."$CTY"
LOG="$DAT".log."$CTY"
XML="$DAT".xml."$CTY"

# Change to working directory
cd /home/peifer/wfdart13 || {
	printf "Error: Cannot change to working directory\n" >> "$LOG"
	exit 1
}

# Fetch the list of files from CDR
wget -q -O "$XML" "http://cdr.eionet.europa.eu/xmlrpc_search_shapefile?country=$CTY"

# Map *.xml and *.dbf files, create index file
/home/peifer/local/bin/xgawk -f /home/peifer/scripts/map_files_xmlrpc.awk "$XML" >> "$IDX"

# Report header, part 1
/home/peifer/local/bin/awk '
BEGIN {
	print	""
	print 	"----------------------------------------"	ORS \
			"     List of shapefiles not checked"		ORS \
			"----------------------------------------"	ORS
}

# NR == FNR does not work, as "$IDX" may be empty
ARGIND == 1 { a[$3] ; next }

$10 ~ /1/ && toupper($4) ~ /DBF.$/ && ! (substr($4,6,length($4)-6) in a) {
	printf "%8d  %s\n", ++cnt, substr($4,6,length($4)-6)
}

END {

	if (! cnt)
		print "(None)"
	else
		printf "\n          (Shapefiles replaced by more recent deliveries or no matching XML data found)\n"

}' "$IDX" "$XML" >> "$LOG"

# Report header, part 2
/home/peifer/local/bin/awk '
BEGIN {
	print	""
	print 	"----------------------------------------"	ORS \
			"       List of shapefiles checked"			ORS \
			"----------------------------------------"	ORS
}

! a[$3]++ { printf "%8d  %s\n", ++cnt, $3 }
END {

	if (! cnt)
		print "(None)"

	printf "\n----------------------------------------\n" }' "$IDX" >> "$LOG"

# Process index file
cat "$IDX" | while read id f1 f2 file_xml file_dbf junk
do
	# Check if both files are readable
	if [[ ! -r "$file_xml" ]] ; then
		printf "\n* * *\nFile NOT found: %s\n* * *\n" "$f1" >> "$LOG"

	elif [[ ! -r "$file_dbf" ]] ; then
			printf "\n* * *\nFile NOT found: %s\n* * *\n" "$f2" >> "$LOG"

	else
		/home/peifer/local/bin/awk -v id="$id" -v f1="$f1" -v f2="$f2" \
		-v file_xml="$file_xml"	-v file_dbf="$file_dbf"	\
		-f /home/peifer/scripts/id_check.awk		\
		<( xsltproc /home/peifer/scripts/wfdart13_codes_to_txt.xsl "$file_xml" ) \
		<( /home/peifer/local/bin/dbfdump -m "$file_dbf" | iconv -f WINDOWS-"$CP" -t UTF-8//IGNORE)
	fi

# Write results to log file
done >> "$LOG"

# Send filtered log through mail
/home/peifer/local/bin/awk '
BEGIN	{ RS = ORS = "----------------------------------------" }
NR < 6	{ print ; next }
/NOT? |Undefined/{

	if (! cnt++)
		print	"\n  Detailed results (error cases only)\n"

	print
}' "$LOG" | mail mette.wolstrup@atkinsglobal.com,jon.maidens@atkinsglobal.com -c hermann.peifer@eea.europa.eu -s "WFD shapefile checking results for country=$CTY  [$DAT]" >> "$LOG" 2>&1
# }' "$LOG" | mail hermann.peifer@eea.europa.eu -s "WFD shapefile checking results for country=$CTY  [$DAT]" >> "$LOG" 2>&1

exit 0

# vim: tw=100 ts=4 sw=4
