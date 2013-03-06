#u-*- encoding: utf-8 -*-
import logging

from flask import Flask, Response, request, redirect, url_for
import jinja2
from tjrj import Processo, feed

env = jinja2.Environment(loader=jinja2.PackageLoader('tjrj', 'templates'))
app = Flask(__name__)

file_handler = logging.FileHandler("webserver.log", encoding="utf-8")
app.logger.addHandler(file_handler)
console_handler = logging.StreamHandler()
app.logger.addHandler(console_handler)

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

if __name__ == '__main__':
    run()
