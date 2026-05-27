import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from config import (
    LOGIN_URL,
    DOWNLOAD_URL,
    HEADERS,
    ZIP_DOWNLOAD_URL,
    directory
)

from auth.login import login

from downloader.rinex import download_rinex


EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


def main():

    session = requests.Session()

    success = login(
        session,
        LOGIN_URL,
        EMAIL,
        PASSWORD
    )

    if not success:
        print("LOGIN FAILED")
        return

    doy = datetime.utcnow().timetuple().tm_yday
    year = datetime.utcnow().year

    stations = [
        "bako",
        "cang",
        "cbik",
        "cdnp",
        "samp",
        "cbda",
        "cmak"
    ]

    for station in stations:

        download_rinex(
            session,
            HEADERS,
            DOWNLOAD_URL,
            station,
            doy,
            year,
            ZIP_DOWNLOAD_URL,
            directory
        )


if __name__ == "__main__":
    main()