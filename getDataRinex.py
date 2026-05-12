import requests
from bs4 import BeautifulSoup
import urllib.parse
import base64

session = requests.Session()

url = "https://srgi.big.go.id/login"
url_station = "https://srgi.big.go.id/middleware-cors/files.FilesService/StasiunV1"


origin = "https://srgi.big.go.id"
user_agent = "grpc-web-javascript/0.1"

# STEP 1: GET login page
res = session.get(url)
print("GET Status:", res.status_code)

soup = BeautifulSoup(res.text, "html.parser")
csrf_token = soup.find("meta", {"name": "csrf-token"})["content"]

print("CSRF Token:", csrf_token)

# ambil cookie
cookies = session.cookies.get_dict()
print("Cookies:", cookies)

# STEP 2: POST login

# decode XSRF-TOKEN (INI PENTING)
xsrf_token = urllib.parse.unquote(cookies.get("XSRF-TOKEN"))

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "X-XSRF-TOKEN": xsrf_token,
    "Referer": url
}

payload = {
    "_token": csrf_token,
    "email": "christian10rks@gmail.com",
    "password": "17Des#/%"
}

login_res = session.post(url, data=payload, headers=headers)

print("POST Status:", login_res.status_code)
print("Final URL:", login_res.url)

# STEP 3: Data Station
# grpc_headers = {
#     "content-type": "application/grpc-web-text",
#     "x-grpc-web": "1",
#     "x-user-agent": user_agent,
#     "origin": origin,
#     "referer": "https://srgi.big.go.id/rinex/v1/download-file-box"
# }

# grpc_payload = b"AAAAAAkKB3N0YXNpdW4="

# station_res = session.post(
#     url_station,
#     headers=grpc_headers,
#     data=grpc_payload
# )

# print("Station Status:", station_res.status_code)

# print("Response Headers:")
# print(station_res.headers)

# print("Response Text:")
# print(station_res.text[:500])

# STEP 4: Get Data By Station
stations = {
    "bako": "bak1",
}

stations_encode = {}

for key, station in stations.items():
    protobuf = b"\x0a" + bytes([len(station)]) + station.encode()

    grpc_frame = (
        b"\x00" + len(protobuf).to_bytes(4, "big") + protobuf
    )

    payload = base64.b64encode(grpc_frame)
    stations_encode[key] = payload.decode()

url_rinex_station = "https://srgi.big.go.id/middleware-cors/files.FilesService/GetFilesV1"

headers_station_rinex = {
    "content-type": "application/grpc-web-text",
    "x-grpc-web": "1",
    "x_user_agent": user_agent,
    "origin": origin,
    "referer": f"https://srgi.big.go.id/rinex/v1.download-file-box/{stations.values()}"
}

response = session.post(
    url_rinex_station,
    headers=headers_station_rinex,
    data=stations_encode["bako"]
)

print(response.status_code)
print(response.text[:5000])