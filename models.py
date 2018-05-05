#!/usr/bin/env python
# -*- coding:utf-8 -*-
from datetime import datetime
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


if __name__ == '__main__':
    pass


