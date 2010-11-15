from naya import Module
from werkzeug import redirect, abort


mod = Module(__name__)


REDIRECTS = (
    ('/post/avtozagruzka-klassov-v-prilozheniyah-na-zend-framework/',
    'blog/2008/09/25/avtozagruzka-klassov-v-prilozheniyah-na-zend-framework',
    'r/zf-autoload'),
    ('/post/unikalniy-nick/', 'r/nick'),
    ('/s/googlee71e35f8e9cbd607.html', 'googlee71e35f8e9cbd607.html')
)


@mod.route('/<path:path>')
def redirector(app, path):
    path = path.rstrip('/')
    for paths in REDIRECTS:
        if path in paths:
            return redirect(paths[0])
    abort(404)
