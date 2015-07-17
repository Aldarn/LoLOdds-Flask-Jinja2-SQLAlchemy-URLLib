# LoL API key
API_KEY = "db60a3be-abf0-479e-b99f-99515a164e55"

# URLs
# TODO: These shouldn't be hardcoded but should instead at least use the API to get the latest versions / links
PROFILE_ICON_BASE_URL = "http://ddragon.leagueoflegends.com/cdn/5.14.1/img/profileicon/"
CHAMPION_BASE_URL = "http://ddragon.leagueoflegends.com/cdn/5.14.1/img/champion/"

# Timeout for when hitting short-term rate limit
RATE_LIMIT_TIMEOUT = 10

# Timeout for when the internet is dropped
NO_INTERNET_TIMEOUT = 10

# Service is unavailable at RIOT's side
SERVICE_UNAVAILABLE_TIMEOUT = 5

# This shouldn't happen very often, but it has been doing...
GATEWAY_TIMEOUT_TIMEOUT = 5