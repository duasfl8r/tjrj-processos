#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
import re
import datetime
import codecs
from urllib.parse import urlparse, parse_qs

import requests

from tjrj import scraping

class Movimento():
    def __init__(self, tipo, data, outros):
        self.tipo = tipo
        self.data = data
        self.outros = outros

    def __str__(self):
        return "<Movimento: {data}, {tipo}>".format(**vars(self))

    def __unicode__(self):
        return self.__str__()

    def from_dict(mov_dict):
        """Transforma o dicionário `mov_dict` em um objeto `Movimento`.

        Tenta extrair o tipo de movimento e uma data.
        """

        data_regex = r'[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9]'

        formato_data = "%d/%m/%Y"
        data = None
        for k, v in mov_dict.items():
            v_ = v.strip()
            if re.match(data_regex, v_):
                data = datetime.datetime.strptime(v_, formato_data)

                del mov_dict[k]
                break

        tipo = None
        if "Tipo do Movimento:" in mov_dict:
            tipo = mov_dict["Tipo do Movimento:"]
            del mov_dict["Tipo do Movimento:"]

        return Movimento(tipo, data, mov_dict)

class Processo():
    """Representa um processo jurídico do TJRJ.

    Atributos:

    - `numero`: o número do processo.
    - `nome`: um nome que identifique o processo.
    - `movimentos`: uma lista com objetos `Movimento`.
    """

    _URL_CONSULTA = "http://srv85.tjrj.jus.br/numeracaoUnica/faces/index.jsp?numProcesso={numero}"
    """URL pra consulta do processo. Mostra os últimos movimentos.

    Essa URL nos redireciona para outra página, usando um *novo número*
    de processo, provavelmente relacionado com o número original do processo.
    """

    _URL_TODOS = "http://srv85.tjrj.jus.br/consultaProcessoWebV2/consultaMov.do?v=2&numProcesso={numero}&acessoIP=internet"
    """URL pra ver todos os movimentos do processo.

    `numProcesso` é um número *diferente* do da `_URL_CONSULTA`.
    """

    def __init__(self, numero, nome=None, fetch=True):
        """Inicializa o processo e busca seus movimentos na web.

        Argumentos:

        - `numero`: o número do processo.
        """

        self.numero = numero
        self.nome = nome if nome else str(numero)
        self.url = Processo._URL_CONSULTA.format(numero=self.numero)

        if fetch:
            self.fetch_movimentos()

    def fetch_movimentos(self):
        req_consulta = requests.get(self.url)
        outro_numero = parse_qs(urlparse(req_consulta.url).query)['numProcesso'][0]
        url_todos = Processo._URL_TODOS.format(numero=outro_numero)
        html = requests.get(url_todos).content

        #html = codecs.open("tjrj/exemplo.html").read()

        mov_dicts = scraping.parse_html(html)

        self.movimentos = list(map(Movimento.from_dict, mov_dicts))

if __name__ == "__main__":
    p = Processo(sys.argv[1])
    feed = p.gerar_feed()
    print(feed)
