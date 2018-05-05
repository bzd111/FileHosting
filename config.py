#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
SQLALCHEMY_DATABASE_URI = 'mysq://web:web@localhost:3306/file'
UPLOAD_FOLDER = '/tmp/permdir'
SQLALCHEMY_TRACK_MODIFICATIONS = False
if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)


if __name__ == '__main__':
    pass


