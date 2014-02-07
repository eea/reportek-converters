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

	# For tab-delimited output
	SUBSEP = "\t"

	# Schemas for file counts
	SCHEMA["01RBDSUCA"] =	"http://water.eionet.europa.eu/schemas/dir200060ec/RBDSUCA_3p0.xsd"
	SCHEMA["02RBMP_POM"] =	"http://water.eionet.europa.eu/schemas/dir200060ec/RBMP_POM_3p0.xsd"
	SCHEMA["03SWB"] =		"http://water.eionet.europa.eu/schemas/dir200060ec/SWB_3p0.xsd"
	SCHEMA["04GWB"] =		"http://water.eionet.europa.eu/schemas/dir200060ec/GWB_3p0.xsd"
	SCHEMA["05ProtArea"] =	"http://water.eionet.europa.eu/schemas/dir200060ec/ProtArea_3p0.xsd"
	SCHEMA["06SWMet"] =		"http://water.eionet.europa.eu/schemas/dir200060ec/SWMethods_3p0.xsd"
	SCHEMA["07GWMet"] =		"http://water.eionet.europa.eu/schemas/dir200060ec/GWMethods_3p0.xsd"
	SCHEMA["08GWMonit"] =	"http://water.eionet.europa.eu/schemas/dir200060ec/GroundWaterMonitoringStations_3p0.xsd"
	SCHEMA["09SWMonit"] =	"http://water.eionet.europa.eu/schemas/dir200060ec/SurfaceWaterMonitoringStations_3p0.xsd"
	SCHEMA["10Monitoring"] ="http://water.eionet.europa.eu/schemas/dir200060ec/Monitoring_3p0.xsd"

	# Strings for file counts
	STRING["11SHP_RBDSU"] =	"_(RBDS?U?C?A?|SU)_"
	STRING["12SHP_RW"] =	"_RWB?_"
	STRING["13SHP_LW"] =	"_LWB?_"
	STRING["14SHP_TW"] =	"_TWB?_"
	STRING["15SHP_CW"] =	"_CWB?_"
	STRING["16SHP_GWB"] =	"_GWB?_"
	STRING["17SHP_PA"] =	"_PA_"
}

# Character data will not be lost, but clear variable first
XMLSTARTELEM	{ chardata = "" }
XMLCHARDATA		{ chardata = $0 }

# Remember relevant attribute values
XMLSTARTELEM == "file" && XMLATTR["isreleased"] {
# XMLSTARTELEM == "file" {

	fid = XMLATTR["id"]
	iup = toupper(fid)
	num = split(iup, F, ".")
	sch = XMLATTR["schema"]

	# Remember all countries/localities seen
	iso = XMLATTR["country_code"]
	loc = XMLATTR["locality"]
	loc = iso SUBSEP loc
	LOC[loc]

	if (sch) {

		FILE[loc,sch]++
		xml_sum++

	} else if (F[num] == "DBF") {

		SHP[loc,fid]

		for (i in STRING) {

			str = STRING[i]

			if (iup ~ str) {
				if (! (i ~ /SHP_.W/ && iup ~ /_PA_/)) {
					FILE[loc,str]++
					shp_sum++
					delete SHP[loc,fid]
				}
			}
		}
	}
}

# Print file mapping
XMLENDELEM == "results" {

	for (i in RBD) {

		# Header row
		if (! hdr++) {

			printf "%s\t%s\t%s", "Country", "Locality", "Title"

			for (j in SCHEMA)
				printf "\t%s", substr(j, 3)

			for (j in STRING)
				printf "\t%s", substr(j, 3)

			print ""
		}

		# File counts

		printf "%s\t%s", i, RBD[i]

		for (j in SCHEMA)
			printf "\t%d", FILE[i,SCHEMA[j]]

		for (j in STRING)
			printf "\t%d", FILE[i,STRING[j]]

		print ""
	}

	# For debugging and double-checks
	if (debug) {

		print ORS "+++ Elements in LOC: not in RBD +++" ORS

		for (i in LOC)
			if (! (i in RBD))
				printf "%8d  %s\n", ++cnt_loc, i

		if (! cnt_loc)
			print "(None)"

		print ORS "+++ Elements in SHP: no STRING found +++" ORS

		for (i in SHP)
			printf "%8d  %s\n", ++cnt_shp, i

		if (! cnt_shp)
			print "(None)"

		print ORS "+++ Sum of counts +++" ORS
		print "XML data:", xml_sum, "+++ Shapefiles:", shp_sum

		print ORS "+++ Elements in FILE: count > 1 +++" ORS

		for (i in FILE)
			if (FILE[i] > 1)
				print i " = " FILE[i]
	}
}

# Print XML errors errors, if any
END {
	if (XMLERROR)
		printf("XMLERROR '%s' at row %d col %d len %d\n",
		XMLERROR, XMLROW, XMLCOL, XMLLEN)
}


# Current list of RBD collections in CDR
BEGIN {

	RBD["AT","AT"] = 			"AT - National level"
	RBD["AT","AT1000"] = 		"AT1000 - Danube"
	RBD["AT","AT2000"] = 		"AT2000 - Rhine"
	RBD["AT","AT5000"] = 		"AT5000 - Elbe"
	RBD["BE","BE"] = 			"BE - National level"
	RBD["BE","BEESCAUT_BR"] = 	"BEEscaut_Schelde_BR - Scheldt"
	RBD["BE","BEESCAUT_RW"] = 	"BEEscaut_RW - Scheldt"
	RBD["BE","BEMAAS_VL"] = 	"BEMaas_VL - Meuse"
	RBD["BE","BEMEUSE_RW"] = 	"BEMeuse_RW - Meuse"
	RBD["BE","BENOORDZEE_FED"] ="BENoordzee_FED - Scheldt"
	RBD["BE","BERHIN_RW"] = 	"BERhin_RW - Rhine"
	RBD["BE","BESCHELDE_VL"] = 	"BESchelde_VL - Scheldt"
	RBD["BE","BESEINE_RW"] = 	"BESeine_RW - Seine"
	RBD["BG","BG"] = 			"BG - National level"
	RBD["BG","BG1000"] = 		"BG1000 - Danube River Basin District"
	RBD["BG","BG2000"] = 		"BG2000 - Black Sea River Basin District"
	RBD["BG","BG3000"] = 		"BG3000 - East Aegean River Basin District"
	RBD["BG","BG4000"] = 		"BG4000 - West Aegean River Basin District"
	RBD["CH","CH"] = 			"CH - National level"
	RBD["CH","CH10"] = 			"CH10 - Rhine"
	RBD["CH","CH50"] = 			"CH50 - Rhone"
	RBD["CH","CH60"] = 			"CH60 - Po"
	RBD["CH","CH80"] = 			"CH80 - Danube"
	RBD["CH","CH90"] = 			"CH90 - Adige"
	RBD["CY","CY"] = 			"CY - National level"
	RBD["CY","CY001"] = 		"CY001 - Cyprus"
	RBD["CZ","CZ"] = 			"CZ - National level"
	RBD["CZ","CZ_RB_1000"] =	"CZ_RB_1000 - Danube"
	RBD["CZ","CZ_RB_5000"] =	"CZ_RB_5000 - Elbe"
	RBD["CZ","CZ_RB_6000"] =	"CZ_RB_6000 - Oder"
	RBD["DE","DE"] = 			"DE - National level"
	RBD["DE","DE1000"] = 		"DE1000 - Danube"
	RBD["DE","DE2000"] = 		"DE2000 - Rhine"
	RBD["DE","DE3000"] = 		"DE3000 - Ems"
	RBD["DE","DE4000"] = 		"DE4000 - Weser"
	RBD["DE","DE5000"] = 		"DE5000 - Elbe"
	RBD["DE","DE6000"] = 		"DE6000 - Odra"
	RBD["DE","DE7000"] = 		"DE7000 - Meuse"
	RBD["DE","DE9500"] = 		"DE9500 - Eider"
	RBD["DE","DE9610"] = 		"DE9610 - Schlei/Trave"
	RBD["DE","DE9650"] = 		"DE9650 - Warnow/Peene"
	RBD["DK","DK"] = 			"DK - National level"
	RBD["DK","DK1"] = 			"DK1 - Jutland and Funen"
	RBD["DK","DK2"] = 			"DK2 - Zealand"
	RBD["DK","DK3"] = 			"DK3 - Bornholm"
	RBD["DK","DK4"] = 			"DK4 - Vidaa-Krusaa"
	RBD["EE","EE"] = 			"EE - National level"
	RBD["EE","EE1"] = 			"EE1 - West Estonia"
	RBD["EE","EE2"] = 			"EE2 - East Estonia"
	RBD["EE","EE3"] = 			"EE3 - Gauja"
	RBD["ES","ES"] = 			"ES - National level"
	RBD["ES","ES010"] = 		"ES010 - Minho-Sil"
	RBD["ES","ES014"] = 		"ES014 - Galician Coast"
	RBD["ES","ES015"] = 		"ES015 - Basque County internal basins"
	RBD["ES","ES016"] = 		"ES016 - Cantabrian"
	RBD["ES","ES020"] = 		"ES020 - Duero"
	RBD["ES","ES030"] = 		"ES030 - Tagus"
	RBD["ES","ES040"] = 		"ES040 - Guadiana"
	RBD["ES","ES050"] = 		"ES050 - Guadalquivir"
	RBD["ES","ES060"] = 		"ES060 - Andalusia Mediterranean Basins"
	RBD["ES","ES063"] = 		"ES063 - Guadalete and Barbate"
	RBD["ES","ES064"] = 		"ES064 - Tinto, Odiel and Piedras"
	RBD["ES","ES070"] = 		"ES070 - Segura"
	RBD["ES","ES080"] = 		"ES080 - Jucar"
	RBD["ES","ES091"] = 		"ES091 - Ebro"
	RBD["ES","ES100"] = 		"ES100 - Internal Basins of Catalonia"
	RBD["ES","ES110"] = 		"ES110 - Balearic Islands"
	RBD["ES","ES120"] = 		"ES120 - Gran Canaria"
	RBD["ES","ES122"] = 		"ES122 - Fuerteventura"
	RBD["ES","ES123"] = 		"ES123 - Lanzarote"
	RBD["ES","ES124"] = 		"ES124 - Tenerife"
	RBD["ES","ES125"] = 		"ES125 - La Palma"
	RBD["ES","ES126"] = 		"ES126 - La Gomera"
	RBD["ES","ES127"] = 		"ES127 - El Hierro"
	RBD["FI","FI"] = 			"FI - National level"
	RBD["FI","FIVHA1"] = 		"FIVHA1 - Vuoksi"
	RBD["FI","FIVHA2"] = 		"FIVHA2 - Kymijoki-Gulf of Finland"
	RBD["FI","FIVHA3"] = 		"FIVHA3 - Kokemäenjoki-Archipelago Sea-Bothnian Sea"
	RBD["FI","FIVHA4"] = 		"FIVHA4 - Oulujoki-Iijoki"
	RBD["FI","FIVHA5"] = 		"FIVHA5 - Kemijoki"
	RBD["FI","FIVHA6"] = 		"FIVHA6 - Tornionjoki (Finnish part)"
	RBD["FI","FIVHA7"] = 		"FIVHA7 - Teno-, Näätämö- and Paatsjoki (Finnish part)"
	RBD["FI","FIWDA"] = 		"FIWDA - Aland islands"
	RBD["FR","FR"] = 			"FR - National level"
	RBD["FR","FRA"] = 			"FRA - Scheldt, Somme and coastal waters of the Channel and the North Sea"
	RBD["FR","FRB1"] = 			"FRB1 - Meuse"
	RBD["FR","FRB2"] = 			"FRB2 - Sambre"
	RBD["FR","FRC"] = 			"FRC - Rhine"
	RBD["FR","FRD"] = 			"FRD - Rhone and Coastal Mediterranean"
	RBD["FR","FRE"] = 			"FRE - Corsica"
	RBD["FR","FRF"] = 			"FRF - Adour, Garonne, Dordogne, Charente and coastal waters of aquitania"
	RBD["FR","FRG"] = 			"FRG - Loire, Brittany and Vendee coastal waters"
	RBD["FR","FRH"] = 			"FRH - Seine and Normandy coastal waters"
	RBD["FR","FRI"] = 			"FRI - Guadeloupe"
	RBD["FR","FRJ"] = 			"FRJ - Martinique"
	RBD["FR","FRK"] = 			"FRK - Guyana (French)"
	RBD["FR","FRL"] = 			"FRL - Reunion Island"
	RBD["GB","GB"] = 			"GB - National level"
	RBD["GB","GBNIIENB"] = 		"GBNIIENB - Neagh Bann"
	RBD["GB","GBNIIENW"] = 		"GBNIIENW - North Western"
	RBD["GB","GBNINE"] = 		"GBNINE - North Eastern"
	RBD["GB","UK01"] = 			"UK01 - Scotland"
	RBD["GB","UK02"] = 			"UK02 - Solway Tweed"
	RBD["GB","UK03"] = 			"UK03 - Northumbria"
	RBD["GB","UK04"] = 			"UK04 - Humber"
	RBD["GB","UK05"] = 			"UK05 - Anglian"
	RBD["GB","UK06"] = 			"UK06 - Thames"
	RBD["GB","UK07"] = 			"UK07 - South East"
	RBD["GB","UK08"] = 			"UK08 - South West"
	RBD["GB","UK09"] = 			"UK09 - Severn"
	RBD["GB","UK10"] = 			"UK10 - Western Wales"
	RBD["GB","UK11"] = 			"UK11 - Dee"
	RBD["GB","UK12"] = 			"UK12 - North West"
	RBD["GB","UKGI17"] = 		"UKGI17 - Gibraltar"
	RBD["GR","GR"] = 			"GR - National level"
	RBD["GR","GR01"] = 			"GR01 - Western Peloponnese"
	RBD["GR","GR02"] = 			"GR02 - Northern Peloponnese"
	RBD["GR","GR03"] = 			"GR03 - Eastern Peloponnese"
	RBD["GR","GR04"] = 			"GR04 - Western Sterea Ellada"
	RBD["GR","GR05"] = 			"GR05 - Epirus"
	RBD["GR","GR06"] = 			"GR06 - Attica"
	RBD["GR","GR07"] = 			"GR07 - Eastern Sterea Ellada"
	RBD["GR","GR08"] = 			"GR08 - Thessalia"
	RBD["GR","GR09"] = 			"GR09 - Western Macedonia"
	RBD["GR","GR10"] = 			"GR10 - Central Macedonia"
	RBD["GR","GR11"] = 			"GR11 - Eastern Macedonia"
	RBD["GR","GR12"] = 			"GR12 - Thrace"
	RBD["GR","GR13"] = 			"GR13 - Crete"
	RBD["GR","GR14"] = 			"GR14 - Aegean Islands"
	RBD["HU","HU"] = 			"HU - National level"
	RBD["HU","HU1000"] = 		"HU1000 - Danube"
	RBD["IE","GBNIIENB"] = 		"GBNIIENB - Neagh Bann"
	RBD["IE","GBNIIENW"] = 		"GBNIIENW - North Western"
	RBD["IE","IE"] = 			"IE - National level"
	RBD["IE","IEEA"] = 			"IEEA - Eastern"
	RBD["IE","IEGBNISH"] = 		"IEGBNISH - Shannon"
	RBD["IE","IESE"] = 			"IESE - South Eastern"
	RBD["IE","IESW"] = 			"IESW - South Western"
	RBD["IE","IEWE"] = 			"IEWE - Western"
	RBD["IT","IT"] = 			"IT - National level"
	RBD["IT","ITA"] = 			"ITA - Eastern Alps"
	RBD["IT","ITB"] = 			"ITB - Po Basin"
	RBD["IT","ITC"] = 			"ITC - Northern Appenines"
	RBD["IT","ITD"] = 			"ITD - Serchio"
	RBD["IT","ITE"] = 			"ITE - Middle Appenines"
	RBD["IT","ITF"] = 			"ITF - Southern Appenines"
	RBD["IT","ITG"] = 			"ITG - Sardinia"
	RBD["IT","ITH"] = 			"ITH - Sicily"
	RBD["LT","LT"] = 			"LT - National level"
	RBD["LT","LT1100"] = 		"LT1100 - Nemunas"
	RBD["LT","LT2300"] = 		"LT2300 - Venta"
	RBD["LT","LT3400"] = 		"LT3400 - Lielupe"
	RBD["LT","LT4500"] = 		"LT4500 - Daugava"
	RBD["LU","LU"] = 			"LU - National level"
	RBD["LU","LU2000"] = 		"LU2000 - Rhine"
	RBD["LU","LU7000"] = 		"LU7000 - Meuse"
	RBD["LV","LV"] = 			"LV - National level"
	RBD["LV","LVDUBA"] = 		"LVDUBA - Daugava"
	RBD["LV","LVGUBA"] = 		"LVGUBA - Gauja"
	RBD["LV","LVLUBA"] = 		"LVLUBA - Lielupe"
	RBD["LV","LVVUBA"] = 		"LVVUBA - Venta"
	RBD["MT","MT"] = 			"MT - National level"
	RBD["MT","MTMALTA"] = 		"MTMalta - Malta"
	RBD["NL","NL"] = 			"NL - National level"
	RBD["NL","NLEM"] = 			"NLEM - Ems"
	RBD["NL","NLMS"] = 			"NLMS - Meuse"
	RBD["NL","NLRN"] = 			"NLRN - Rhine"
	RBD["NL","NLSC"] = 			"NLSC - Scheldt"
	RBD["NO","NO"] = 			"NO - National level"
	RBD["NO","NO1101"] = 		"NO1101 - Moere and Romsdal"
	RBD["NO","NO1102"] = 		"NO1102 - Troendelag"
	RBD["NO","NO1103"] = 		"NO1103 - Nordland"
	RBD["NO","NO1104"] = 		"NO1104 - Troms"
	RBD["NO","NO1105"] = 		"NO1105 - Finnmark"
	RBD["NO","NO5101"] = 		"NO5101 - Glomma"
	RBD["NO","NO5102"] = 		"NO5102 - West Bay"
	RBD["NO","NO5103"] = 		"NO5103 - Agder"
	RBD["NO","NO5104"] = 		"NO5104 - Rogaland"
	RBD["NO","NO5105"] = 		"NO5105 - Hordaland"
	RBD["NO","NO5106"] = 		"NO5106 - Sogn and Fjordane"
	RBD["NO","NOFIVHA5"] = 		"NOFIVHA5 - Kemijoki"
	RBD["NO","NOFIVHA6"] = 		"NOFIVHA6 - Tornionjoki (Finnish part)"
	RBD["NO","NOSE1"] = 		"NOSE1 - Bothnian Bay"
	RBD["NO","NOSE1TO"] = 		"NOSE1TO - Torne River"
	RBD["NO","NOSE2"] = 		"NOSE2 - Bothnian Sea"
	RBD["NO","NOSE5"] = 		"NOSE5 - Skagerrak and Kattegat"
	RBD["PL","PL"] = 			"PL - National level"
	RBD["PL","PL1000"] = 		"PL1000 - Danube"
	RBD["PL","PL2000"] = 		"PL2000 - Vistula"
	RBD["PL","PL3000"] = 		"PL3000 - Swieza"
	RBD["PL","PL4000"] = 		"PL4000 - Jarft"
	RBD["PL","PL5000"] = 		"PL5000 - Elbe"
	RBD["PL","PL6000"] = 		"PL6000 - Odra"
	RBD["PL","PL6700"] = 		"PL6700 - Ucker"
	RBD["PL","PL7000"] = 		"PL7000 - Pregolya"
	RBD["PL","PL8000"] = 		"PL8000 - Nemunas"
	RBD["PL","PL9000"] = 		"PL9000 - Dniestr"
	RBD["PT","PT"] = 			"PT - National level"
	RBD["PT","PTRH1"] = 		"PTRH1 - Minho and Lima"
	RBD["PT","PTRH10"] = 		"PTRH10 - Madeira"
	RBD["PT","PTRH2"] = 		"PTRH2 - Cavado, Ave and Leca"
	RBD["PT","PTRH3"] = 		"PTRH3 - Douro"
	RBD["PT","PTRH4"] = 		"PTRH4 - Vouga, Mondego and Lis"
	RBD["PT","PTRH5"] = 		"PTRH5 - Tagus and Western Basins"
	RBD["PT","PTRH6"] = 		"PTRH6 - Sado and Mira"
	RBD["PT","PTRH7"] = 		"PTRH7 - Guadiana"
	RBD["PT","PTRH8"] = 		"PTRH8 - Algarve Basins"
	RBD["PT","PTRH9"] = 		"PTRH9 - Azores"
	RBD["RO","RO"] = 			"RO - National level"
	RBD["RO","RO1000"] = 		"RO1000 - Danube"
	RBD["SE","SE"] = 			"SE - National level"
	RBD["SE","SE1"] = 			"SE1 - Bothnian Bay"
	RBD["SE","SE1TO"] = 		"SE1TO - Torne river"
	RBD["SE","SE2"] = 			"SE2 - Bothnian Sea"
	RBD["SE","SE3"] = 			"SE3 - North Baltic"
	RBD["SE","SE4"] = 			"SE4 - South Baltic"
	RBD["SE","SE5"] = 			"SE5 - Skagerrak and Kattegat"
	RBD["SE","SENO1102"] = 		"SENO1102 - Troendelag"
	RBD["SE","SENO1103"] = 		"SENO1103 - Nordland"
	RBD["SE","SENO1104"] = 		"SENO1104 - Troms"
	RBD["SE","SENO5101"] = 		"SENO5101 - Glomma"
	RBD["SI","SI"] = 			"SI - National level"
	RBD["SI","SI_RBD_1"] = 		"SI_RBD_1 - Danube"
	RBD["SI","SI_RBD_2"] = 		"SI_RBD_2 - North Adriatic"
	RBD["SK","SK"] = 			"SK - National level"
	RBD["SK","SK30000"] = 		"SK30000 - Vistula"
	RBD["SK","SK40000"] = 		"SK40000 - Danube"
}

# vim: tw=100 ts=4 sw=4
