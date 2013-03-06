#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import sys

import codecs
import argparse
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from tjrj import Processo, feed, webserver

verbose = False

def error(msg):
    sys.stderr.write('ERRO:', msg)

def info(msg):
    if verbose:
        print(msg)

def _salvar_feeds(args):
    config = _get_config(args.config)

    for section in config.sections():
        p = Processo(numero=config.get(section, 'numero'), nome=section)
        info('Gerando feed: {nome} ({numero})'.format(**vars(p)))
        dir = args.diretorio if args.diretorio else config.get(section, 'diretorio_feeds')
        feed.salvar(p, dir)

def _webserver(args):
    webserver.app.run(host='127.0.0.1', port=int(args.port), debug=True)

def _get_config(path):
    if os.path.isdir(path):
        error('O arquivo de configuração {path} é um diretório.'.format(**vars()))
        exit(1)

    config = configparser.ConfigParser()
    config.readfp(codecs.open(path, encoding="utf-8"))

    return config

def run(argv=None):
    global verbose

    if not argv:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description='Exibe informações sobre processos jurídicos do TJRJ')
    parser.add_argument('-c', '--config', default=os.path.expanduser('~/.tjrj-processos'),
            help='Arquivo de configuração com os processos a serem usados')
    parser.add_argument('-v', '--verbose', action='store_true',
            help='Mostra mensagens de informação')
    subparsers = parser.add_subparsers()

    parse_feed = subparsers.add_parser('salvar-feeds', help='Salva em disco feeds atom dos movimentos dos processos')
    parse_feed.set_defaults(func=_salvar_feeds)
    parse_feed.add_argument('-d', '--diretorio',
            help='Diretório onde serão colocados os arquivos XML (sobrepõe o arquivo de configuração')

    parse_feed = subparsers.add_parser('webserver', help='Inicia um servidor web que serve feeds de processos')
    parse_feed.add_argument('-p', '--port', default="5000",
            help='Porta onde o servidor web escutará')
    parse_feed.set_defaults(func=_webserver)

    args = parser.parse_args(argv)

    if args.verbose:
        verbose = True

    args.func(args)

if __name__ == '__main__':
    run(sys.argv[1:])
