#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import uuid
import magic
from datetime import datetime


try:
    from urllib import quote_plus # python2
except ImportError:
    from urllib.parse import quote_plus # python3


import cropresize2
import short_url
from PIL import Image
from flask import abort, request
from werkzeug.utils import cached_property


from libs.mimes import AUDIO_MIMES, IMAGE_MIMES, VIDEO_MIMES
from libs.utils import get_file_md5, get_file_path
from ext import db


class PasteFile(db.Model):

    """Docstring for PasteFile. """
    __table__ = 'PasterFile'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(5000), nullable=True)
    filehash = db.Column(db.String(128), nullable=False, unique=True)
    filemd5 = db.Column(db.String(128), nullable=False, unique=True)
    uploadtime = db.Column(db.DataTime, nullable=False)
    mimetype = db.Column(db.String(256), nullable=False)
    size = db.Column(db.Integer, nullable=False)


    def __init__(self, filename='', mimetype='application/octet-stream', size=0, filehash=None, filemd5=None):
        """TODO: to be defined1.

        Kwargs:
            filename (TODO): TODO
            mimetype (TODO): TODO
            size (TODO): TODO
            filehash (TODO): TODO
            filemd5 (TODO): TODO
        """

        self.uploadtime = datetime.now()
        self._filename = filename
        self._mimetype = mimetype
        self._size = size
        self._filehash = filehash
        self._filemd5 = filemd5

    @staticmethod
    def _hash_filename(filename):
        _, _, suffix = filename.rpartition('.')
        return '%s.%s' %(uuid.uuid4().hex, suffix)

    @cached_property
    def symlink(self):
        return short_url.encode_url(self.id)

    @classmethod
    def get_by_symlink(cls, symlink, code=404):
        id = short_url.decode_url(cls.id)
        return cls.query.filter_by(id=id).first() or abort(code)

    @classmethod
    def get_by_filehash(cls, filehash, code=404):
        return cls.query.filter_by(filehash=filehash).first() or abort(code)

    @classmethod
    def get_by_md5(cls, filemd5, code=404):
        return cls.query.filter_by(filemd5=filemd5).first() or abort(code)

    @classmethod
    def create_by_upload(cls, upload_file):
        rst = cls(upload_file.filename, upload_file.mimetype, 0)
        upload_file.save(rst.path)
        with open(rst.path, 'rb') as f:
            filemd5 = get_file_md5(f)
            upload_file = cls.get_by_md5(filemd5)
            if upload_file:
                os.remove(rst.path)
                return upload_file
        filestat = os.stat(rst.path)
        rst._size = filestat.st_size
        rst._filemd5 = filemd5

    @classmethod
    def create_by_old_paste(cls, filehash):
        filepath = get_file_path(filehash)
        mimetype = magic.from_file(filepath, mime=True)
        filestat = os.stat(filepath)
        size = filestat.st_size
        rst = cls(filehash, mimetype, size, filehash=filehash)
        return rst

    @property
    def path(self):
        return get_file_path(self.filehash)


    def get_url(self, subtype, is_symlink=False):
        hash_or_link = self.symlink if is_symlink else self.filehash
        return 'http://{host}/{subtye}/{hash_or_link}'.format(
            host=request.host, subtype=subtype, hash_or_link=hash_or_link
        )

    @property
    def url_i(self):
        return self.get_url('i')

    @property
    def url_p(self):
        return self.get_url('g')

    @property
    def url_s(self):
        return self.get_url('d')

    @property
    def is_image(self):
        return self.mimetype in IMAGE_MIMES

    @property
    def is_audio(self):
        return self.mimetype in AUDIO_MIMES

    @property
    def is_video(self):
        return self.mimetype in VIDEO_MIMES

    @property
    def is_pdf(self):
        return self.mimetype == 'application/pdf'

    @property
    def image_size(self):
        if self.is_image:
            f = open(self.path, 'rb')
            im = Image.open(f)
            return im.size
        return (0, 0)

    @property
    def quoteurl(self):
        return quote_plus(self.url_i)

    @classmethod
    def rsize(cls, old_paste, weight, height):
        assert old_paste.is_image, TypeError("Unspported Image Type")
        f = open(old_paste.path, 'rb')
        im = Image.open(f)
        img = cropresize2.crop_resize(im, (int(weight), int(height)))
        rst = cls(old_paste._filename, old_paste._mimetype, 0)
        img.save(rst.path)
        filestat = os.stat(rst.path)
        rst.size = filestat.st_size
        return rst

    @property
    def type(self):
        for t in ('image', 'pdf', 'video', 'audio'):
            if getattr(self, 'is_' + t):
                return t
        return 'binary'


if __name__ == '__main__':
    pass


