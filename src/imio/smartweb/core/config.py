import os

DIRECTORY_URL = os.environ.get("DIRECTORY_URL", "https://annuaire.enwallonie.be")
EVENTS_URL = os.environ.get("EVENTS_URL", "https://agenda.enwallonie.be")
NEWS_URL = os.environ.get("NEWS_URL", "https://actualites.enwallonie.be")
# Set to the Vite dev server URL (e.g. http://localhost:2000) to load the
# webcomponents bundle from `npm run watch` instead of the built production
# bundle. Leave empty in production.
VITE_DEV_URL = os.environ.get("VITE_DEV_URL", "")
