from flask import Flask, render_template, request, views, redirect,Response

from services import *
from functools import wraps




app = Flask(__name__)


def authenticate():
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route("/page")


class UserUrlView(views.MethodView):
    def get(self):
        return render_template('index.html')
    def post(self):
        short_url = get_short_url(request)
        return render_template('index.html', short_url=short_url)

@app.route("/sh.ly/<short_url>",methods=['GET'])

def ShortUrl(short_url):
    info = short_answer(short_url)
    if info[1] == 1:
        return redirect(info[0], code=302)
    if info[1] == 2:
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return redirect(info[0], code=302)
    if info[1] == 3:
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return redirect(info[0], code=302)

'''
1 - публичная ссылка
2 - ссылка общего доступа
3 - приватная ссылка
'''
app.add_url_rule('/', view_func=UserUrlView.as_view('user'))

if __name__ == '__main__':
    app.run()

