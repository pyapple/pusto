from datetime import datetime

from naya.testing import raises
from pymongo.errors import DuplicateKeyError

from . import app, drop_db
from pusto.ext.translit import slugify


def setup():
    drop_db()


def is_created(doc):
    assert isinstance(doc['created'], datetime)


def is_markuped(doc):
    assert doc.is_valid('markup')
    assert doc['markup'] == u'rst'
    doc['markup'] = 'textile'
    assert not doc.is_valid('markup')
    doc['markup'] = u'markdown'
    assert doc.is_valid('markup'), doc.validation_errors


def test_user(name=u'naspeh'):
    user = app.db.User()
    is_created(user)
    assert not user.is_valid()
    user.update({'email': u'%s@ya' % name, 'name': name})
    user.save()
    assert user['_id']
    return user


def test_node(title=u'test title'):
    node = app.db.Node()
    is_created(node)
    assert not node.is_valid()

    name = u'naya'
    user = test_user(name)
    node.update({'title': title, 'content': test_text(user), 'owner': user})
    node.save()
    assert node['slug'] == slugify(title)
    assert node['_id']
    assert node['content']['_id']
    assert node['owner']['_id']

    node['wrong'] = True
    assert not node.is_valid()

    node2 = app.db.Node()
    node2['title'] = title
    raises(DuplicateKeyError, lambda: node2.save())

    raises(DuplicateKeyError, lambda: test_user(name))
    return node


def test_text(user=None):
    bit = app.db.TextBit()
    is_created(bit)
    is_markuped(bit)
    assert not bit.is_valid()
    bit['body'] = u'test body'
    bit.save()
    assert bit['_id']

    text = app.db.Text()
    is_created(text)
    is_markuped(text)
    assert text.is_valid()
    text.update({'bits': [bit], 'owner': user or test_user(u'nayavu')})
    text.save()
    assert text['_id']
    assert text['owner']['_id']
    assert text['bits'][0]['_id']
    return text
