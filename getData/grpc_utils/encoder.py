import struct


def encode_varint(value):

    out = b""

    while value > 127:
        out += struct.pack(
            "B",
            (value & 0x7F) | 0x80
        )
        value >>= 7

    out += struct.pack("B", value)

    return out


def protobuf_field(field_number, data):

    tag = (field_number << 3) | 2

    return (
        encode_varint(tag)
        + encode_varint(len(data))
        + data
    )