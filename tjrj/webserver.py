#u-*- encoding: utf-8 -*-
from flask import Flask, Response, request, redirect, url_for
import jinja2
from tjrj import Processo, feed

env = jinja2.Environment(loader=jinja2.PackageLoader('tjrj', 'templates'))
app = Flask(__name__)

@app.route('/')
def index():
    if request.method == 'GET' and request.args:
        if request.args['submit'] == 'Feed':
            return redirect(url_for('processo_feed',
                numero=request.args['numeroProcesso']))
        else:
            return redirect(url_for('processo',
                numero=request.args['numeroProcesso']))
    else:
        template = env.get_template("web/index.html")
        return Response(template.render())

@app.route('/<numero>/feed')
def processo_feed(numero):
    processo = Processo(numero)
    return Response(feed.gerar(processo), mimetype='application/atom+xml')

@app.route('/<numero>/')
def processo(numero):
    processo = Processo(numero)
    template = env.get_template("web/processo.html")

    return Response(template.render(processo=processo))

def run(*args, **kwargs):
    app.run(debug=True)

if __name__ == '__main__':
    run()
