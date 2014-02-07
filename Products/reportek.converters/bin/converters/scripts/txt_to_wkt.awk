# Text to formatted WKT quick hack
# Hermann, March 2009

# Each char is a field
BEGIN { FS = "" }

{
	for (i=1; i<=NF; i++) {

		# Decide if to add a line break
		str = $i ~ /[[:upper:]]/ && p ~ /,$/ ? "\n"  : ""

		# Calculate depth
		if (str) {
			if (p ~ /[^]],$/)	depth+=4
			else if (p ~ /]],$/)	depth-=4
		}

		# Print string, line breaks and indentation
		printf "%s%*s%s", str, (str ? depth : ""), "", $i

		# Remember previous
		p = p $i
	}
}

# Print a line break
END { print "" }

