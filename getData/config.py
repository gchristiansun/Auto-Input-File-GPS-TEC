BASE_URL = "https://srgi.big.go.id"

LOGIN_URL = f"{BASE_URL}/login"

ZIP_DOWNLOAD_URL = f"{BASE_URL}/zip_middleware_cors/"

DOWNLOAD_URL = (
    f"{BASE_URL}/middleware-cors/"
    "files.FilesService/DownloadAllConversiMoveToSrgi"
)

HEADERS = {
    "content-type": "application/grpc-web-text",
    "x-grpc-web": "1",
    "x-user-agent": "grpc-web-javascript/0.1",
    "user-agent": "Mozilla/5.0",
    "origin": BASE_URL,
    "referer": f"{BASE_URL}/rinex/v1/carts",
    "accept": "application/grpc-web-text"
}

directory = "E:/rinex/"