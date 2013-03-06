#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Author: Lucas Teixeira <lucas@lucasteixeira.com>
# Copyright: MIT License

"""
Processos jurídicos do TJRJ e seus movimentos.

Classes definidas:

- `Processo`, um processo jurídico
- `Movimento`, um movimento dentro de um processo

Como usar esse módulo
=====================

1. Importe a classe `Processo`.

2. Crie um objeto de processo fornecendo seu número e opcionalmente um nome::

        p = Processo("0007765-23.2011.8.19.0037", "Telemar")

   Ao criar o objeto, ele automaticamente buscará os movimentos na Web. Para impedir esse comportamento, passe `fetch=True`. Posteriormente, os movimentos podem ser baixados através do método `Processo.fetch_movimentos()`

3. A lista de  movimentos podem ser acessada pelo atributo `p.movimentos`.
"""

import sys
import re
import datetime
import codecs

try:
    from urllib.parse import urlparse, parse_qs
except ImportError:
    from urlparse import urlparse, parse_qs

import requests

from tjrj import scraping

class Movimento():
    
    """
    Um movimento de um processo jurídico do TJRJ.

    Cada movimento tem os atributos:

    - `tipo`: uma string com o tipo de movimento
    - `data`: um objeto `datetime.datetime` com a data do movimento
    - `outros`: um dicionário contendo outras informações específicas de
      cada tipo de movimento.
    """

    def __init__(self, tipo, data, outros):
        self.tipo = tipo
        self.data = data
        self.outros = outros

    def __str__(self):
        return "<Movimento: {data}, {tipo}>".format(**vars(self))

    def __unicode__(self):
        return self.__str__()

    @classmethod
    def from_dict(cls, mov_dict):
        """
        Transforma o dicionário `mov_dict` em um objeto `Movimento`.

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

        for k, v in mov_dict.items():
            if k and k[-1] == ":":
                del mov_dict[k]
                k = k[:-1]
                mov_dict[k] = v

        return Movimento(tipo, data, mov_dict)

class Processo():
    """
    Representa um processo jurídico do TJRJ.

    Atributos:

    - `numero`: o número do processo.
    - `nome`: um nome que identifique o processo.
    - `movimentos`: uma lista com objetos `Movimento`.
    """

    _URL_CONSULTA = "http://srv85.tjrj.jus.br/numeracaoUnica/faces/index.jsp?numProcesso={numero}"
    """
    URL pra consulta do processo. Mostra os últimos movimentos.

    Essa URL nos redireciona para outra página, usando um *novo número*
    de processo, relacionado com o número original do processo de alguma
    maneira misteriosa.
    """

    _URL_TODOS = "http://srv85.tjrj.jus.br/consultaProcessoWebV2/consultaMov.do?v=2&numProcesso={numero}&acessoIP=internet"
    """
    URL pra ver todos os movimentos do processo.

    `numProcesso` é um número *diferente* do da `_URL_CONSULTA`.
    """

    def __init__(self, numero, nome=None, fetch=True):
        """
        Inicializa o processo e busca seus movimentos na web.

        Argumentos:

        - `numero`: o número do processo.
        - `nome`: o nome dado ao processo. Se esse argumento não for
          passado, o nome do processo é igual ao seu número.
        - `fetch`: se `True`, baixa automaticamente os movimentos da
          Web.
        """

        self.numero = numero
        self.nome = nome if nome else str(numero)
        self.url = Processo._URL_CONSULTA.format(numero=self.numero)

        if fetch:
            self.fetch_movimentos()

    def __str__(self):
        return u"{nome} - {numero}".format(**vars(self))

    def fetch_movimentos(self):
        """
        Baixa os movimentos da página Web do processo e armazena no
        objeto `movimentos`.

        Usa o módulo `tjrj.scraping` pra fazer o "parsing" do HTML e
        extrair os movimentos.
        """

        req_consulta = requests.get(self.url)
        url_query = parse_qs(urlparse(req_consulta.url).query)
        outro_numero = url_query['numProcesso'][0]
        url_todos = Processo._URL_TODOS.format(numero=outro_numero)
        html = requests.get(url_todos).content

        #html = codecs.open("tjrj/exemplo.html").read()

        mov_dicts = scraping.parse_html(html)

        self.movimentos = list(map(Movimento.from_dict, mov_dicts))
