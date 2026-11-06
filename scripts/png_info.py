"""Read PNG dimensions and colour type without third-party dependencies."""
import struct


def png_info(path):
    with open(path, 'rb') as stream:
        header = stream.read(33)
    if len(header) != 33 or header[:8] != b'\x89PNG\r\n\x1a\n' or header[12:16] != b'IHDR':
        raise ValueError(f'Invalid PNG header: {path}')
    width, height = struct.unpack('>II', header[16:24])
    if not width or not height:
        raise ValueError(f'Invalid PNG dimensions: {path}')
    return (width, height), header[25]
