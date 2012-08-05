# -*- encoding: utf-8 -*-
from flask import Flask, Response
import jinja2
from tjrj import Processo, feed

env = jinja2.Environment(loader=jinja2.PackageLoader('tjrj', 'templates'))
app = Flask(__name__)

@app.route('/')
def ola_mundo():
    return 'Olá, mundo!'

@app.route('/<numero>/feed')
def processo_feed(numero):
    processo = Processo(numero)
    return Response(feed.gerar(processo), mimetype='application/atom+xml')

@app.route('/<numero>/')
def processo(numero):
    processo = Processo(numero)
    template = env.get_template("web.html")

    return Response(template.render(processo=processo))

def run(*args, **kwargs):
    app.run(debug=True)

if __name__ == '__main__':
    run()
