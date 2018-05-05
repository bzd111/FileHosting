#!/usr/bin/env python
# -*- coding:utf-8 -*-
import Flask

from ext import db, mako


app = Flask(__name__)
app.config.from_object('config')

mako.init_app(app)
db.init_app(app)


if __name__ == '__main__':
    pass


