import json
import base64
import struct

from grpc_utils.encoder import protobuf_field


def build_payload(
    station,
    doy,
    year,
    batch_id="31412"
):

    filename = (
        f"{station}"
        f"{doy:03d}0."
        f"{str(year)[2:]}d.gz"
    )

    json_part = json.dumps(
        [{
            "doy": doy,
            "status_file": True,
            "bg_selected": "bg-primary",
            "lock": True,
            "filename": filename,
            "path": f"{year}/{station}",
            "type": "nowYear",
            "stasiun": station,
            "total": None
        }],
        separators=(",", ":")
    ).encode()

    file_part = json.dumps(
        [filename]
    ).encode()

    proto = b""
    proto += protobuf_field(1, json_part)
    proto += protobuf_field(2, file_part)
    proto += protobuf_field(4, batch_id.encode())

    grpc_frame = (
        b"\x00"
        + struct.pack(">I", len(proto))
        + proto
    )

    return (
        base64.b64encode(grpc_frame).decode(),
        filename
    )