import os

DIRECTORY_URL = os.environ.get("DIRECTORY_URL", "https://annuaire.enwallonie.be")
EVENTS_URL = os.environ.get("EVENTS_URL", "https://agenda.enwallonie.be")
NEWS_URL = os.environ.get("NEWS_URL", "https://actualites.enwallonie.be")
WCA_URL = os.environ.get(
    "WCA_URL", "https://agents.wallonie-connect.be/idp/oidc/token/"
)

TS_BASIC_AUTH_USER = os.environ.get("TS_BASIC_AUTH_USER", None)
TS_BASIC_AUTH_PASSWORD = os.environ.get("TS_BASIC_AUTH_PASSWORD", None)
