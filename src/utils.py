from resources.config import PROFILE_ICON_BASE_URL, CHAMPION_BASE_URL

def getProfileIconUrl(iconId):
	return "%s%s.png" % (PROFILE_ICON_BASE_URL, iconId)

def getChampionImageUrl(championName):
	return "%s%s" % (CHAMPION_BASE_URL, championName)
