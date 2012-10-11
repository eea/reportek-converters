BEGIN	{
		FIELDWIDTHS = "18 31 21 36 48"
		print ORS "AWK test result for file",ARGV[1] ORS
	}

a[$1]++	{
		print "*Duplicate id*", $1,$3,$4 ; d=1
	}

END	{
		if ( ! d )
			print "No duplicate IDs found."
	}
