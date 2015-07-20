# LoL API key
# TODO: Shouldn't have committed this; remove this from the repo and then regenerate it
API_KEY = "db60a3be-abf0-479e-b99f-99515a164e55"

# URLs
# TODO: These shouldn't be hardcoded but should instead at least use the API to get the latest versions / links
PROFILE_ICON_BASE_URL = "http://ddragon.leagueoflegends.com/cdn/5.14.1/img/profileicon/"
CHAMPION_BASE_URL = "http://ddragon.leagueoflegends.com/cdn/5.14.1/img/champion/"

# Timeout for when hitting short-term rate limit
RATE_LIMIT_TIMEOUT = 10

# Timeout for when the internet is dropped
NO_INTERNET_TIMEOUT = 10

# Timeout for when a request fails for some reason that should be retried
RETRY_REQUEST_TIMEOUT = 5

# This seems to be right but I couldn't find any documentation saying otherwise...
# Well the colours might be the wrong way around, but it doesn't really matter
# TODO: Figure out if this is right and/or ever changes
PURPLE_TEAM_ID = 100
BLUE_TEAM_ID = 200