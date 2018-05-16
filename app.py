#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

from flask import Flask, abort, request, jsonify, redirect, render_template

from ext import db, mako
from models import PasteFile
from libs.utils import humanize_bytes, get_file_path


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
    if uploaded_file:
        paste_file = PasteFile.create_by_upload(uploaded_file)
        db.session.add(paste_file)
        db.session.commit()
        width, height = paste_file.image_size

        return jsonify({
            'url': paste_file.url_i,
            'short_url': paste_file.url_s,
            'origin_filename': paste_file.filename,
            'hash': paste_file.filehash,
            'width': width,
            'height': height
        })
    return abort(404)


@app.route('/p/<filehash>')
def perview(filehash):
    paste_file = PasteFile.get_by_filehash(filehash)
    if not paste_file:
        filepath = get_file_path(filehash)
        if not(os.path.exists(filepath)) and not(os.path.islink(filepath)):
            return abort(404)
        paste_file = PasteFile.create_by_old_paste(filehash)
        db.session.add(paste_file)
        db.session.commit()


@app.route('/s/<symlink>')
def s(symlik):
    paste_file = PasteFile.get_by_symlik(symlik)
    return redirect(paste_file.url_p)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


