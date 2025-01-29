import os
import dotenv

dotenv.load_dotenv()

REGEX: str = os.getenv("REGEX", "")

PATH_TO_WEBSITE: str = os.getenv("PATH_TO_WEBSITE", "")

PATH_TO_WEBSITE_NEWS: str = os.getenv("PATH_TO_WEBSITE_NEWS", "")

PATH_TO_SAVE: str = os.getenv("PATH_TO_SAVE", "")