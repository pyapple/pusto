# -*- coding: utf-8 -*-
from naya import UrlMap


map = UrlMap(__name__)


@map.route('/', defaults={'id': 'new'})
@map.route('/<id>')
def main(app, id):
    text = prepare(id, app)
    bit = prepare_bit('new', text, app)
    return app.to_template('editor/main.html', text=text, active=bit)


@map.route('/<id>/delete')
def delete(app, id):
    text = prepare(id, app)
    for bit in text['bits']:
        bit.delete()
    text.delete()
    return app.redirect(app.url_for(':editor.main'))


@map.route('/<id>/bit')
def bit(app, id):
    if not app.request.form:
        app.abort(403)

    action = app.request.form['action']
    bit_id = app.request.form['bit']
    text = prepare(id, app)
    bit = prepare_bit(bit_id, text, app)
    if action == 'apply':
        if bit['_id'] is None:
            del bit['_id']
        insert = app.request.form['insert']
        if insert:
            text['bits'].remove(bit)
            parent = app.request.form['parent']
            parent = app.db.TextBit.find_one(app.object_id(parent))
            parent = text['bits'].index(parent)
            parent = parent if insert == 'before' else parent + 1
            text['bits'].insert(parent, bit)

        bit['body'] = app.request.form['body']
        bit.save()
        text.save()
        prepare_bit('new', text, app)
    elif action == 'delete' and bit_id != 'new':
        bit.delete()
        text['bits'].remove(bit)
        text.save()
        bit = prepare_bit('new', text, app)
    elif action == 'reset':
        return bit['body']
    return app.from_template('editor/partial.html', 'partial')(text, bit, app)


def prepare(id, app):
    if id == 'new':
        text = app.db.Text()
    else:
        text = app.db.Text.find_one(app.object_id(id))
    if not text:
        return app.abort(404)
    return text


def prepare_bit(id, text, app):
    if id == 'new':
        bit = app.db.TextBit()
        bit['body'] = ''
        bit['_id'] = None
        text['bits'].append(bit)
    else:
        bit = app.db.TextBit.find_one(app.object_id(id))
    if not bit:
        return app.abort(404)
    return bit