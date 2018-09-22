def cleanUniques(uniques):
	for i, unique in enumerate(uniques):
		unique = unique.split("(", maxsplit = 1)[0]
		unique = unique.rstrip()
		uniques[i] = unique
	uniques = sorted(set(uniques))
	return uniques