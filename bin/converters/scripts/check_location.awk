# XMLgawk script to process EPER 2004 XML data
# Usage: xgawk -f scriptfile.awk datafile(s).xml
# Hermann, December 2008

# Load the XML extension
@load xml

# Some hard-coded values
BEGIN {
	XMLMODE		= 1
	XMLCHARSET	= "UTF-8"
	OFS = SUBSEP	= "\t"

	# Definition of relevant child elements under element Facility
	split("NationalID FacilityName Address PostCode City Latitude Longitude", E, " ")

	# Add element names to lookup array ELEMENTS
	for (i in E)
		ELEMENTS[E[i]]
}

# Clear Country variable, to be on the safe side
XMLDEPTH == 1 && XMLSTARTELEM {	Country = "" }

# Character data will not be lost, but clear variable first
XMLSTARTELEM { chardata = "" }
XMLCHARDATA  { chardata = normalize_space($0) }

# For each country
XMLENDELEM == "Country" {

	# Remember country code
	Country = chardata

	# Print a report header
	prefix = Country ~ /^(CZ|NL|UK)$/ ? "the " : ""
	print "<html><body><pre>"
	print "QA report for EPER facility locations from " prefix name[Country]
}

# Remember character data of Facility child elements
XMLDEPTH == 4 && XMLENDELEM in ELEMENTS { val[XMLENDELEM] = chardata }

# Print collected values, 1 row per facility
XMLENDELEM == "Facility" { 

	# Count number of facilities, by country
	COUNT[Country]++

	# For testing and debugging
	# if ( COUNT[Country] > 7 ) nextfile

	# Geocode requests
	geocode()

	# For a clean start with the next facility
	delete val
}

# Some summary statistics at the end of the XML document
XMLENDELEM && XMLDEPTH == 1 {

	print ORS "Summary of facility location QA for " prefix name[Country]
	printf "%5d %s\n", COUNT[Country],"facilities checked, of which:"

	for (i in COUNT) {
		split(i, I, SUBSEP)
		if (I[2]) printf "   %5d %s\n", COUNT[i], I[2]
	}
	print "</pre></body></html>"
}

# Print XMLERRORS, if any
END {
	if (XMLERROR)
		printf("XMLERROR '%s' at row %d col %d len %d\n",
			XMLERROR, XMLROW, XMLCOL, XMLLEN) > "/dev/stdout"
}

# Remove leading and trailing [[:space:]] characters
function trim(str) {
	sub(/^[[:space:]]+/, "", str)
	if (str) sub(/[[:space:]]+$/, "", str)
	return str
}

# Trim first, then reduce internal sequences
# of [[:space:]] characters to a single space
function normalize_space(str) {
	str = trim(str)
	if (str) gsub(/[[:space:]]+/, " ", str)
	return str
}

# Function for geocoding
function geocode(    REQ,req,command,prec,gresult,yresult,count) {

	# Print reported values
	print ORS COUNT[Country]
	print Country " " val["NationalID"] " " val["FacilityName"]
	print val["Address"] ", " val["PostCode"] " " val["City"]
	print "Reported: " sprintf("%-10s", val["Latitude"]) " " val["Longitude"]

	# Use both Google and Yahoo geocoder
	REQ[construct_request("Google")]
	REQ[construct_request("Yahoo!")]

	# Make the actual geocoding requests
	for (req in REQ) {

		command = "wget -O - -q -t 3 '" req "'"

		while ( (command | getline) > 0) {

			# For processing a Google geocoding response

			if (XMLSTARTELEM == "AddressDetails") {
				prec = precision[XMLATTR["Accuracy"]+0]
				gresult = limit[prec] ",Google," prec
			}

			if (XMLCHARDATA && XMLPATH ~ /coordinates$/) {

				# Value format: longitude,latitude,height
				split($0, C, ",")

				# Add Lat/Lon, but exclude results w/o precision limits
				gresult = prec in limit ? gresult "," C[2] "," C[1] : "" 
			}

			# For processing a Yahoo! geocoding response

			if (XMLSTARTELEM == "Result") {
				prec = XMLATTR["precision"]

				# Exclude results w/o precision limits
				if (prec in limit)
					yresult = limit[prec] ",Yahoo!," prec
			}

			# Add Lat/Lon, but only if yresult non-empty
			if (XMLCHARDATA && XMLPATH ~ /(Latitude|Longitude)$/)
				yresult = yresult ? yresult "," $0 : "" 

			# Break after first placemark (Google) or result (Yahoo!)
			if (XMLENDELEM ~ /^(Placemark|Result)$/)
				break
		}
		close(command)
	}

	# Decide which geocoding result is best. If both have equal precision:
	# Take Google result, as Yahoo! results often come with warnings
	if ( gresult && yresult )
		print distance( yresult+0 < gresult+0 ? yresult : gresult )
	else if ( gresult )
		print distance(gresult)
	else if ( yresult )
		print distance(yresult)
	else {
		print "No geocoding result" ORS
		COUNT[Country,"No geocoding result"]++
	}
}

# Function to construct a geocoding request
function construct_request(geocoder,    url,q) {

	if (geocoder == "Google") {

		# Base URL
		url = "http://maps.google.com/maps/geo?output=xml&sensor=false&key=ABQIAAAAjcez8Ywjqro5wKSVPOGm8hRHRyN95irczJxvGrIM2epZrRh-exTHa3aS8wpDR25kKqPYFVKFAOUo_Q"

		# Start with Address and PostCode
		q = "&q=" val["Address"] "," val["PostCode"]

		# Add City value, if not already part of Address
		if (! index(q, val["City"]))
			q = q " " val["City"]

		# Add country name and gl parameter
		q = q	"," name[Country]
		q = q	"&gl=" Country

	} else if (geocoder == "Yahoo!") {

		# Base URL
		url  = "http://local.yahooapis.com/MapsService/V1/geocode?appid=YD-9G7bey8_JXxQP6rxl.fBFGgCdNjoDMACQA--"

		# Add Address, PostCode, City and country
		q =	"&street="	val["Address"]
		q = q	"&zip="		val["PostCode"]
		q = q	"&city="  	val["City"]
		q = q	"&state="	name[Country]
		q = q	"&country="	Country
	}
	return url clean(q)
}

# Function to replace unwanted characters with "+"
function clean(str) {

	gsub(/[^[:alnum:]&,=]+/, "+", str)
	# gsub(/[\(\)/[:space:]]+/, "+", str)

	return str
}

# Function to calculate the great circle distance, i.e. the shortest
# distance over the earth's surface using the Haversine formula.
# It assumes a spherical earth, ignoring ellipsoidal effects,
# which is accurate enough for most purposes. See also at:
# http://mathforum.org/library/drmath/view/51879.html
# Geocoding result format "limit,geocoder,precision,latitude,longitude"
#
function distance(result,    G,lat1,lon1,lat2,lon2,dlat,dlon,a,c,d,eval) {

	# Split the input values
	split(result, G, ",")

	# Convert degrees into radians
	lat1 = G[4] * pi / 180
	lon1 = G[5] * pi / 180

	lat2 =  val["Latitude"]  * pi / 180
	lon2 =  val["Longitude"] * pi / 180

	dlat = lat2 - lat1
	dlon = lon2 - lon1

	# Calculate the distance
	a = sin(dlat/2)^2 + cos(lat1) * cos(lat2) * sin(dlon/2)^2
	c = 2 * atan2(sqrt(a), sqrt(1-a))
	d = r * c

	# Distance rounded to nearest 10 m
	d = sprintf("%.2f", d) + 0

	 eval = ( d < limit[G[3]] ? "Not " : "" ) "Suspicious"
	 COUNT[Country,eval]++

	result =		"Geocoded: " sprintf("%-10s", G[4]) " " G[5] 
	result = result ORS	"Geocoder: " G[2] " with " G[3] " precision"
	result = result ORS	"Distance: " d " km - " eval

	return result
}


# Hard coded values and lookup arrays
BEGIN {
	# Lookup array for country names
        name["AL"]="Albania"
        name["AT"]="Austria"
        name["BA"]="Bosnia and Herzegovina"
        name["BE"]="Belgium"
        name["BG"]="Bulgaria"
        name["CH"]="Switzerland"
        name["CY"]="Cyprus"
        name["CZ"]="Czech Republic"
        name["DE"]="Germany"
        name["DK"]="Denmark"
        name["EE"]="Estonia"
        name["ES"]="Spain"
        name["FI"]="Finland"
        name["FR"]="France"
        name["GB"]="United Kingdom"
        name["UK"]="United Kingdom"
        name["GR"]="Greece"
        name["HR"]="Croatia"
        name["HU"]="Hungary"
        name["IE"]="Ireland"
        name["IS"]="Iceland"
        name["IT"]="Italy"
        name["LI"]="Liechtenstein"
        name["LT"]="Lithuania"
        name["LU"]="Luxembourg"
        name["LV"]="Latvia"
        name["MC"]="Monaco"
        name["ME"]="Montenegro"
        name["MK"]="FYR of Macedonia"
        name["MT"]="Malta"
        name["NL"]="Netherlands"
        name["NO"]="Norway"
        name["PL"]="Poland"
        name["PT"]="Portugal"
        name["RO"]="Romania"
        name["RS"]="Serbia"
        name["SE"]="Sweden"
        name["SI"]="Slovenia"
        name["SK"]="Slovakia"
        name["TR"]="Turkey"

	# Translate Google's GGeoAddressAccuracy levels into Yahoo! precision names
	precision[0] = "unknown"
	precision[1] = "country"
	precision[2] = "state"
	precision[3] = "state"
	precision[4] = "city"
	precision[5] = "zip"
	precision[6] = "street"
	precision[7] = "street"
	precision[8] = "address"
	precision[9] = "address"

	# Limits for suspicious distances (in km)
	limit["city"]    = 10
	limit["zip"]     =  5
	limit["street"]  =  3
	limit["address"] =  1

	# Definition of pi
	pi = atan2(0, -1)

	# The earth's mean radius
	a = 6378.137	# Equatorial radius (in km)
	b = 6356.752	# Polar radius (in km) 
	r = (a + b) / 2	# ~ 6367 km
}
