# XMLgawk script to map files in WFD envelopes
# Input: a .../envelope/xml file from CDR
#
# Hermann, March 2010

# Load the XML extension 
@load xml

BEGIN { 
	# Set XMLMODE so that the XML parser reads strictly
	# compliant XML data. Convert characters to XMLCHARSET
	XMLMODE = 1 
	XMLCHARSET = "UTF-8" 

	# Strings for file name mapping
	STRING["1RB"] = STRING["2SU"] = "_RBD_"
	STRING["3PA"] = "_PA_"
	STRING["4GW"] = "_GWB_"
	STRING["5CW"] = "_SWB_CW_"
	STRING["6LW"] = "_SWB_LW_"
	STRING["7RW"] = "_SWB_RW_"
	STRING["8TW"] = "_SWB_TW_"

	# Schemas for file name mapping
	SCHEMA["1RB"] = SCHEMA["2SU"] = \
	"http://water.eionet.europa.eu/schemas/dir200060ec/RBDSUCA_3p0.xsd"

	SCHEMA["3PA"] = "http://water.eionet.europa.eu/schemas/dir200060ec/ProtArea_3p0.xsd"
	SCHEMA["4GW"] =	"http://water.eionet.europa.eu/schemas/dir200060ec/GWB_3p0.xsd"

	SCHEMA["5CW"] = SCHEMA["6LW"] = SCHEMA["7RW"] =  SCHEMA["8TW"] = \
	"http://water.eionet.europa.eu/schemas/dir200060ec/SWB_3p0.xsd"
}

# Character data will not be lost, but clear variable first
XMLSTARTELEM	{ chardata = "" }
XMLCHARDATA		{ chardata = $0 }

# Remember the URL
XMLENDELEM == "link"	{ link = chardata }

# Remember files by schema or file name suffix
XMLSTARTELEM == "file"	{

	n = split(XMLATTR["name"], F, ".")

	if (XMLATTR["schema"])
		FILE[XMLATTR["schema"]] = XMLATTR["name"]

	else if (toupper(F[n]) == "DBF")
		for (i in STRING)
			if (toupper(XMLATTR["name"]) ~ STRING[i])
				FILE[STRING[i]] = XMLATTR["name"]
}

# Print file mapping
XMLENDELEM   == "envelope" {

	for (i in STRING)
		if (FILE[SCHEMA[i]] && FILE[STRING[i]])
			print substr(i,2), link "/" FILE[SCHEMA[i]], link "/" FILE[STRING[i]]
}

# Print XML errors errors, if any
END {
	if (XMLERROR)
		printf("XMLERROR '%s' at row %d col %d len %d\n",
		XMLERROR, XMLROW, XMLCOL, XMLLEN)
}

# vim: tw=100 ts=4 sw=4
