import urllib.parse
from bs4 import BeautifulSoup


def login(session, url, email, password):

    res = session.get(url)

    soup = BeautifulSoup(res.text, "html.parser")

    csrf_token = soup.find(
        "meta",
        {"name": "csrf-token"}
    )["content"]

    cookies = session.cookies.get_dict()

    xsrf_token = urllib.parse.unquote(
        cookies.get("XSRF-TOKEN")
    )

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-XSRF-TOKEN": xsrf_token,
        "Referer": url
    }

    payload = {
        "_token": csrf_token,
        "email": email,
        "password": password
    }

    login_res = session.post(
        url,
        data=payload,
        headers=headers
    )

    print("LOGIN:", login_res.status_code)

    return login_res.ok