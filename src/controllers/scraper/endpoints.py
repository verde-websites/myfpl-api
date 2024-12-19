"""Create an enum for all fpl endpoints"""

from enum import Enum
BASE_FPL_URL = "https://fantasy.premierleague.com/api/"
class FPLEndpoints(Enum):
    """FPL Endpoints"""
    BOOTSTRAP_STATIC = BASE_FPL_URL + "bootstrap-static"
    PLAYER_SUMMARY = BASE_FPL_URL + "element-summary"
    FIXTURES = BASE_FPL_URL + "fixtures"
    LIVE = BASE_FPL_URL + "live"
    LOGIN = "https://users.premierleague.com/accounts/login/"
    LOGIN_REDIRECT = "https://fantasy.premierleague.com/a/login"
    LOGOUT = BASE_FPL_URL + "logout"
    TEAM_CARD = BASE_FPL_URL + "entry"
    ME = BASE_FPL_URL + "me"