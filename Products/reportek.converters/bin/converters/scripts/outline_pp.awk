# Print an XML document's outline (based on outline.awk)
# plus: print attribute values and character data
# Usage: xgawk [-v w=<num>] -f outline_plus.awk file.xml
# Hermann, March 2010

# Load the XML extension
@load xml

# Run in strict XML mode, define character set and width
BEGIN { XMLMODE = 1 ; XMLCHARSET = "UTF-8" ; if (!w) w=35 }

# Check for obvious errors (must be the first clause!)
ERRNO { XmlCheckError() }

XMLSTARTELEM {

	# In case the preceding element is a complex element 
	if (x && XMLDEPTH > x)
		print ""

	# Print element name and attribute values (if any)
	printf "%*s%s", 2*XMLDEPTH-2, "", XMLSTARTELEM

	# Reset attribute length
	att_length = 0

		if (NF)
			for (i=1; i<=NF; i++) {
				printf " %s='%s'", $i, XMLATTR[$i]
				att_length = att_length + length($i) + length(XMLATTR[$i]) + 4
			}

	# Remember XMLDEPTH 
	x = XMLDEPTH

	# Clear chardata variable
	chardata = ""

	next
}

# Remember character data
XMLCHARDATA { chardata = normalize_space($0) ; next }

# Print character data
XMLENDELEM && XMLDEPTH == x { printf "%*s'%s'\n",w-(XMLDEPTH*2)-length(XMLENDELEM)-att_length, "", chardata ; next }

# Print XML errors, if any
END { XmlCheckError() }

# XMLgawk error reporting needs some redesign.
# Interim code (from Manuel Collado): uses both 
# ERRNO and XMLERROR to generate consistent messages 
function XmlCheckError() {

	if (XMLERROR) {
		printf "\n%s:%d:%d:(%d) %s\n",
		FILENAME, XMLROW, XMLCOL, XMLLEN, XMLERROR > "/dev/stderr"

	} else if (ERRNO) {
		printf "\n%s\n", ERRNO > "/dev/stderr"
		ERRNO = ""
	}
	exit 1
}

# Remove leading and trailing [[:space:]] characters
function trim(str)
{
	sub(/^[[:space:]]+/, "", str)
	if (str "") sub(/[[:space:]]+$/, "", str)
	return str
}

# Trim first, then reduce internal sequences
# of [[:space:]] characters to a single space
function normalize_space(str)
{
	str = trim(str)
	if (str "") gsub(/[[:space:]]+/, " ", str)
	return str
}

# vim: tw=100 ts=4 sw=4
