#!/bin/bash

# Check codes in WFD Art. 13 deliveries: XML data vs shapefiles
# Shell script to download checklist.txt, start id_check.awk
# and mail the results to a list of recipients
#
# Hermann, March 2010

DAT=$(date '+%Y%m%d_%H%M')
IDX="$DAT".idx
LOG="$DAT".log

cd /home/peifer/wfdart13 || {
	printf "Error: Cannot change to working directory\n" > "$LOG"
	exit 1
}

# wget -N -o download.log "http://water.eionet.europa.eu/schemas/dir200060ec/resources/checklist.txt"
wget -N -o download.log "http://www.eionet.europa.eu/testfolder/checklist.txt"

NEW=$(grep -c checklist.txt.*saved download.log)

if [[ -s checklist.txt && $NEW > 0 ]] ; then

	awk '$1 !~ /^#/ && (NF == 1 || NF == 3)' checklist.txt | while read str1 str2 str3
	do
		if [[ -z "$str2" && -z "$str3" ]] ; then
		
			wget -q -O - "$str1"/xml |
			/home/peifer/local/bin/xgawk -f /home/peifer/scripts/map_files.awk >> "$IDX"

		else

			echo "$str1" "$str2" "$str3" >> "$IDX"

		fi
	done

	awk 'NF == 3' "$IDX" | while read id f1 f2
	do
		# Get the physicalpath of Report Documents
		file_xml=$(wget -q -O - "$f1"/physicalpath)
		file_dbf=$(wget -q -O - "$f2"/physicalpath)

		# Check if both files are readable
		if [[ ! -r "$file_xml" ]] ; then
			printf "\n* * *\nFile not found: %s\n* * *\n" "$f1" >> "$LOG"

		elif [[ ! -r "$file_dbf" ]] ; then
			printf "\n* * *\nFile not found: %s\n* * *\n" "$f2" >> "$LOG"

		# Use modern xgawk, old awk doesn't know /dev/fd/<n> files
		else
			/home/peifer/local/bin/xgawk -v id="$id" -v f1="$f1" -v f2="$f2" \
			-v file_xml="$file_xml"	-v file_dbf="$file_dbf"	\
			-f /home/peifer/scripts/id_check.awk		\
			<( xsltproc /home/peifer/scripts/wfdart13_codes_to_txt.xsl "$file_xml" ) \
			<( /home/peifer/local/bin/dbfdump -m "$file_dbf" )
		fi
	# Write results to log file and send them by mail
	done | tee -a "$LOG" | grep -v ^path:.*cdr/var |
	mail hermann.peifer@eea.europa.eu -s "WFD shapefile checking results $DAT" 2>&1
	# mail HelpdeskWFD@atkinsglobal.com -c hermann.peifer@eea.europa.eu -s "WFD shapefile checking results $DATE" 2>&1

else
	printf "Nothing to do: remote file empty or no newer than local file\n" > "$LOG"
fi

exit 0

# vim: tw=100 ts=4 sw=4
