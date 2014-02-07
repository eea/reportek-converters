# XMLgawk script to map files in WFD envelopes
# CDR input: xmlrpc_search_shapefile[?country=cc]
#
# Hermann, March 2010

# Load the XML extension 
@load xml

BEGIN { 
	# Set XMLMODE so that the XML parser reads strictly
	# compliant XML data. Convert characters to XMLCHARSET
	XMLMODE = 1
	XMLCHARSET = "UTF-8" 

	# Strings for file mapping
	STRING["AA"] = "(RBDS?U?C?A?|SU|_RB_)"
	# STRING["AA"] = "_RBD_"
	STRING["PA"] = "PA"
	STRING["GW"] = "GWB?"
	STRING["CW"] = "CWB?"
	STRING["LW"] = "LWB?"
	STRING["RW"] = "RWB?"
	STRING["TW"] = "TWB?"

	# Schemas for file mapping
	SCHEMA["AA"] = "http://water.eionet.europa.eu/schemas/dir200060ec/RBDSUCA_3p0.xsd"
	SCHEMA["PA"] = "http://water.eionet.europa.eu/schemas/dir200060ec/ProtArea_3p0.xsd"
	SCHEMA["GW"] = "http://water.eionet.europa.eu/schemas/dir200060ec/GWB_3p0.xsd"

	SCHEMA["CW"] = SCHEMA["LW"] = SCHEMA["RW"] =  SCHEMA["TW"] = \
	"http://water.eionet.europa.eu/schemas/dir200060ec/SWB_3p0.xsd"
}

# Character data will not be lost, but clear variable first
XMLSTARTELEM	{ chardata = "" }
XMLCHARDATA		{ chardata = $0 }

# Remember relevant attribute values
XMLSTARTELEM == "file" && XMLATTR["isreleased"] {
# XMLSTARTELEM == "file" {

	iup = toupper(XMLATTR["id"])
	num = split(iup, F, ".")

	iso = XMLATTR["country_code"]
	loc = XMLATTR["locality"]
	loc = iso SUBSEP loc
	LOC[loc]

	sch = XMLATTR["schema"]
	unx = XMLATTR["unixtime"]
	url = XMLATTR["url"]
	phy = XMLATTR["physicalpath"]

	if (sch) {

		if (unx > TIME[loc,sch] + 0) {
			FILE[loc,sch] = url
			PATH[loc,sch] = phy
			TIME[loc,sch] = unx
		}

	} else if (F[num] == "DBF") {

		for (i in STRING) {

			str = STRING[i]

			if (iup ~ str && unx >= TIME[loc,str] + 0) {
	
				# There can be several files...
				if (unx == TIME[loc,str]) {
					FILE[loc,str] = FILE[loc,str] "|" url
					PATH[loc,str] = PATH[loc,str] "|" phy
				} else {
					FILE[loc,str] = url
					PATH[loc,str] = phy
				}

				TIME[loc,str] = unx
			}
		}
	}
}

# Print file mapping
XMLENDELEM == "results" {

	for (i in LOC) {

		split(i, I, SUBSEP)
		prefix = tolower(I[1]) "_" tolower(I[2])

		for (j in STRING) {

			key1 = i SUBSEP SCHEMA[j]
			key2 = i SUBSEP STRING[j]

			if (key1 in FILE && key2 in FILE) {

				# Handle cases with multiple dbf files
				x = split(FILE[key2], DBF, "|")
				y = split(PATH[key2], PHY, "|")

				if (x != y) {
					print "Non-matching number of FILE and PATH array elements" > "/dev/stderr"
					exit 1
				}

				# File name and envelope id for XML data
				z = split(FILE[key1], TMP, "/")
				xml_file = TMP[z]
				xml_env  = TMP[z-1]

				for (k=1; k<=x; k++) {

					# File name and envelope id for shapefile
					z = split(DBF[k], TMP, "/")
					dbf_file = TMP[z]
					sub(/(dbf|DBF)$/, "shp", dbf_file)
					dbf_env  = TMP[z-1]

					# Print RBDSU mappings twice (2 checks)
					if (j == "AA") {

						print	"RB", FILE[key1], DBF[k], PATH[key1], PHY[k], I[1], I[2],
								xml_file, prefix "_" xml_env "_" strftime("%Y%m%d", TIME[key1]) ".zip",
								dbf_file, prefix "_" dbf_env "_" strftime("%Y%m%d", TIME[key2]) ".zip"

						print	"SU", FILE[key1], DBF[k], PATH[key1], PHY[k], I[1], I[2],
								xml_file, prefix "_" xml_env "_" strftime("%Y%m%d", TIME[key1]) ".zip",
								dbf_file, prefix "_" dbf_env "_" strftime("%Y%m%d", TIME[key2]) ".zip"

					# Print other mappings once (1 check only)
					} else {
						# Avoid false _PA_GW_, _PA_LW_, etc. mappings
						if (! (j ~ /W/ && DBF[k] ~ /_PA_/))
							print   j, FILE[key1], DBF[k], PATH[key1], PHY[k], I[1], I[2],
									xml_file, prefix "_" xml_env "_" strftime("%Y%m%d", TIME[key1]) ".zip",
									dbf_file, prefix "_" dbf_env "_" strftime("%Y%m%d", TIME[key2]) ".zip"
					}
				}
			}
		}
	}

	#	For debugging
	if (debug) {

		print ORS "+++ Elements in LOC +++" ORS

		for (i in LOC)
			print i

		print ORS "+++ Elements in TIME +++" ORS

		for (i in TIME)
			print i " = " TIME[i]

		print ORS "+++ Elements in FILE +++" ORS

		for (i in FILE)
			print i " = " FILE[i]
	}
}

# Print XML errors errors, if any
END {
	if (XMLERROR)
		printf("XMLERROR '%s' at row %d col %d len %d\n",
		XMLERROR, XMLROW, XMLCOL, XMLLEN)
}

# vim: tw=100 ts=4 sw=4
