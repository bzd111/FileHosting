#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os


from werkzeug import SharedDataMiddleware
from flask import Flask, abort, request, jsonify, redirect, send_file


from ext import db, mako
from models import PasteFile


app = Flask(__name__)
app.config.from_object('config')

mako.init_app(app)
db.init_app(app)


if __name__ == '__main__':
    pass


