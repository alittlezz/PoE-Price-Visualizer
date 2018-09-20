import bs4 as bs
import urllib.request

def getUniqueNames():
	uniques = []
	appendUniques(uniques, "http://pathofexile.gamepedia.com/List_of_unique_accessories")
	appendUniques(uniques, "https://pathofexile.gamepedia.com/List_of_unique_body_armours")
	appendUniques(uniques, "http://pathofexile.gamepedia.com/List_of_unique_boots")
	appendUniques(uniques, "http://pathofexile.gamepedia.com/List_of_unique_gloves")
	appendUniques(uniques, "http://pathofexile.gamepedia.com/List_of_unique_helmets")
	appendUniques(uniques, "http://pathofexile.gamepedia.com/List_of_unique_shields")
	appendUniques(uniques, "https://pathofexile.gamepedia.com/List_of_unique_axes")
	appendUniques(uniques, "https://pathofexile.gamepedia.com/List_of_unique_bows")
	appendUniques(uniques, "http://pathofexile.gamepedia.com/List_of_unique_claws")
	appendUniques(uniques, "http://pathofexile.gamepedia.com/List_of_unique_daggers")
	appendUniques(uniques, "https://pathofexile.gamepedia.com/List_of_unique_fishing_rods")
	appendUniques(uniques, "http://pathofexile.gamepedia.com/List_of_unique_maces")
	appendUniques(uniques, "http://pathofexile.gamepedia.com/List_of_unique_staves")
	appendUniques(uniques, "http://pathofexile.gamepedia.com/List_of_unique_swords")
	appendUniques(uniques, "http://pathofexile.gamepedia.com/List_of_unique_wands")
	appendUniques(uniques, "http://pathofexile.gamepedia.com/List_of_unique_flasks")
	appendUniques(uniques, "http://pathofexile.gamepedia.com/List_of_unique_jewels")
	appendUniques(uniques, "http://pathofexile.gamepedia.com/List_of_unique_maps")
	return uniques

def appendUniques(uniques, pageUrl):
	sauce = urllib.request.urlopen(urllib.request.Request(pageUrl, headers = {"User-Agent" : "Wat"})).read();
	soup = bs.BeautifulSoup(sauce, 'lxml')

	table = soup.findAll("div", {"id" : "mw-content-text"})
	table = table[0]
	table = table.findAll("span", {"class" : "c-item-hoverbox__activator"})
	for item in table:
		uniques.append(item.a["title"])
