from resources.config import PROFILE_ICON_BASE_URL, CHAMPION_BASE_URL, BLUE_TEAM_ID, PURPLE_TEAM_ID

def getProfileIconUrl(iconId):
	return "%s%s.png" % (PROFILE_ICON_BASE_URL, iconId)

def getChampionImageUrl(championName):
	return "%s%s" % (CHAMPION_BASE_URL, championName)

def getTeamName(teamId):
	if teamId == BLUE_TEAM_ID:
		return "BLUE"
	elif teamId == PURPLE_TEAM_ID:
		return "PURPLE"
	return "UNKNOWN"