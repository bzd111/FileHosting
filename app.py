#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os


from werkzeug import SharedDataMiddleware
from flask import Flask, abort, request, jsonify, redirect, send_file, render_template


from ext import db, mako
from models import PasteFile
from libs.utils import humanize_bytes

app = Flask(__name__)
app.config.from_object('config')

mako.init_app(app)
db.init_app(app)


@app.route('/r/<img_hash>')
def rsize(img_hash):
    w = request.args['w']
    h = request.args['h']

    old_paste = PasteFile.get_by_filehash(img_hash)
    new_paste = PasteFile.rsize(old_paste, w, h)
    return new_paste.url_i


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        w = request.form.get('w')
        h = request.form.get('h')
        if not uploaded_file:
            return abort(404)

        if w and h:
            paste_file = PasteFile(uploaded_file, w, h)
        else:
            paste_file = PasteFile.create_by_upload(uploaded_file)
        db.session.add(paste_file)
        db.session.commit()

        return jsonify({
            'url_d': paste_file.url_d,
            'url_i': paste_file.url_i,
            'url_s': paste_file.url_s,
            'url_p': paste_file.url_p,
            'filename': paste_file.filename,
            'size': humanize_bytes(paste_file.size),
            'time': str(paste_file.uploadtime),
            'type': paste_file.type,
            'quoteurl': paste_file.quoteurl
        })
    return render_template('index.html', **locals())


@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allowe-Headers'] = 'Content-Type'
    return response


@app.route('/j', methods=['POST'])
def j():
    uploaded_file = request.files['file']
    pass

if __name__ == '__main__':
    pass


