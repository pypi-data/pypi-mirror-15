"""Reddit Endpoints.
"""
from pytsite import router as _router, http as _http
from ._session import AuthSession as _AuthSession

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def authorize(args: dict, inp: dict):
    session = _AuthSession(inp.get('state'))
    error = inp.get('error')
    if error:
        _router.session().add_error(error)

    return _http.response.Redirect(_router.url(session.redirect_uri, query=inp))
