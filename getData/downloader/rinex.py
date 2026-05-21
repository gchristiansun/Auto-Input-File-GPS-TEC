from grpc_utils.payload import build_payload
from utils.decoder import decode_grpc_web
import base64
import struct


def download_rinex(
    session,
    headers,
    url,
    station,
    doy,
    year,
    url_download
):

    payload, filename = build_payload(
        station,
        doy,
        year
    )

    r = session.post(
        url,
        headers=headers,
        data=payload
    )

    print(f"[{station}] STATUS:", r.status_code)

    if not r.ok:
        return

    decoded = base64.b64decode(r.text)

    # compressed_flag = decoded[0]

    msg_len = struct.unpack(">I", decoded[1:5])[0]

    msg = decoded[5:5+msg_len]

    try:
        zip_name = (
            msg.decode(errors="ignore")
            .replace("@", "")
            .strip()
        )

        print("ZIP NAME:", zip_name)

    except Exception as e:
        print("Decode error:", e)
        return
    
    download_url = (
        url_download
        + zip_name
    )

    print("DOWNLOAD URL:", download_url)

    zip_res = session.get(download_url)

    print("ZIP STATUS:", zip_res.status_code)

    if zip_res.status_code == 200:

        with open(zip_name, "wb") as f:
            f.write(zip_res.content)

        print("ZIP saved:", zip_name)

    else:
        print("Failed download ZIP")