import base64
import struct


def decode_grpc_web(response_text):

    decoded = base64.b64decode(response_text)

    msg_len = struct.unpack(
        ">I",
        decoded[1:5]
    )[0]

    return decoded[5:5 + msg_len]