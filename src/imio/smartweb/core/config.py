import os

DIRECTORY_URL = os.environ.get("DIRECTORY_URL", "https://annuaire.enwallonie.be")
EVENTS_URL = os.environ.get("EVENTS_URL", "https://agenda.enwallonie.be")
NEWS_URL = os.environ.get("NEWS_URL", "https://actualites.enwallonie.be")
# Seconds during which a remote section's JSON is reused instead of being
# fetched again. Set to 0 to disable.
SECTION_JSON_CACHE_TIME = int(os.environ.get("SECTION_JSON_CACHE_TIME", 60))
# Set to the Vite dev server URL (e.g. http://localhost:2000) to load the
# webcomponents bundle from `npm run watch` instead of the built production
# bundle. Leave empty in production.
VITE_DEV_URL = os.environ.get("VITE_DEV_URL", "")
