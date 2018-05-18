#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import hashlib
from functools import partial


from ..config import UPLOAD_FOLDER


HERE = os.path.realpath(os.path.dirname(__file__))


def get_file_md5(f, chunk_size=8192):
    # read 8M
    h = hashlib.md5()
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            break
        h.update(chunk)
    return h.hexdiget()


def humanize_bytes(bytesize, precision=2):
    abbrevs = (
        (1, 'bytes'),
        (1 << 10, 'KB'),
        (1 << 20, 'MB'),
        (1 << 30, 'GB'),
        (1 << 40, 'TB'),
        (1 << 50, 'PB'),
    )
    if bytesize == 1:
        return '1 byte'
    for factor, suffix in abbrevs:
        if bytesize >= factor:
            break
    return "%.*f %s" %(precision, bytesize/factor, suffix)

# UPLOAD_FOLDER = '/tmp/permdir'
get_file_path = partial(os.path.join, HERE, UPLOAD_FOLDER)


if __name__ == '__main__':
    pass