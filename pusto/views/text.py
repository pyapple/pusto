from naya.helpers import marker


@marker.route('/text/new', defaults={'id': 'new'})
@marker.route('/text/<id>/edit')
def edit(app, id):
    node = None
    if 'node' in app.request.args:
        node = app.request.args['node']
    text, node = prepare(app, id, node)
    bit = prepare_bit(app, 'new', text)
    bit = active_bit(app, text, bit)
    return app.to_template('text/edit.html', text=text, active=bit, node=node)


@marker.route('/text/<id>/delete')
def delete(app, id):
    text = prepare(app, id)[0]
    text.delete()
    return app.redirect(app.url_for(':text.edit'))


@marker.route('/text/<id>', defaults={'src': False})
@marker.route('/text/<id>/text', defaults={'src': 'text'})
@marker.route('/text/<id>/html', defaults={'src': 'html'})
def show(app, id, src):
    text, node = prepare(app, id)
    return app.maybe_partial('#text-show-body', app.to_template(
        'text/show.html', text=text, node=node, src=src
    ))


@marker.authorized()
@marker.route('/texts/')
def roll(app):
    texts = app.db.Text.find({'owner': app.user.dbref})
    return app.to_template('text/list.html', texts=texts)


@marker.route('/text/<id>/bit')
def bit(app, id):
    data = app.request.form
    if not data:
        app.abort(403)

    action = data['action']
    bit_id = data['bit']
    text, node = prepare(app, id)
    bit = prepare_bit(app, bit_id, text)
    if action == 'apply':
        if bit['_id'] is None:
            del bit['_id']
        insert = 'insert' in data and data['insert'] or None
        if insert:
            text['bits'].remove(bit)
            parent = data['parent']
            parent = app.db.TextBit.by_id(parent)
            parent = text['bits'].index(parent)
            parent = parent if insert == 'before' else parent + 1
            text['bits'].insert(parent, bit)

        type = 'type' in data and data['type'] or None
        if type:
            bit['type'] = type

        bit['body'] = data['body'].strip()
        bit.save_all(text)
        text.save()

        prepare_bit(app, 'new', text)
    elif action == 'delete' and bit['_id']:
        bit.delete()
        text.reload()
        bit = prepare_bit(app, 'new', text)
    elif action == 'reset' and bit['_id']:
        prepare_bit(app, 'new', text)

    fill_session(app, text, bit)
    return app.maybe_partial('#text-edit', app.to_template(
        'text/edit.html', text=text, node=node, active=bit
    ))


def prepare(app, id, node_id=None):
    node = None
    if id == 'new':
        text = app.db.Text()
        text.update({'owner': app.user})
    else:
        text = app.db.Text.by_id(id) if id else None
        node = text and text.node or None
    if text and text['owner'] and text['owner'] != app.user:
        return app.abort(403)

    if not node and node_id:
        node = app.db.Node.by_id(node_id)
        if not node:
            return app.abort(404)
        text.save()
        node['content'] = text
        node.save()
    if not text:
        return app.abort(404)
    return text, node or app.db.Node()


def prepare_bit(app, id, text):
    if id == 'new':
        bit = app.db.TextBit()
        bit['body'] = ''
        bit['_id'] = None
        text['bits'].append(bit)
    else:
        bit = app.db.TextBit.by_id(id) if id else None
    if not bit:
        return app.abort(404)
    return bit


def active_bit(app, text, bit):
    if '_id' not in text:
        return bit

    text_id = str(text['_id'])
    if 'texts' in app.session and text_id in app.session['texts']:
        active = app.session['texts'][text_id]
        active = text.bit_by_id(active)
        bit = active and active or bit
    return bit


def fill_session(app, text, bit):
    app.session.setdefault('texts', {})
    app.session['texts'][str(text['_id'])] = str(bit['_id'])
