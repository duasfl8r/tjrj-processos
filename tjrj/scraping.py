#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from bs4 import BeautifulSoup

def parse_html(html):
    def strip_elem(e):
        return str(e).strip()

    def non_empty_children(elem):
        if hasattr(elem, "children"):
            return list(filter(strip_elem, elem.children))
        else:
            return None

    def parse_movimento(movimento):
        def parse_tr(tr):
            tds = non_empty_children(tr)
            if tds and len(tds) == 2:
                conteudos = map(lambda f: f.text.strip(), tds)
                return tuple(conteudos)
            else:
                return ()

        def items_do_movimento(movimento):
            while movimento.next_sibling:
                if hasattr(movimento, "name"):
                    yield movimento

                sibling = movimento.next_sibling
                if (hasattr(sibling, "attrs") and
                    "tipoMovimento" in sibling.attrs.get("class", [])):
                    break

                movimento = movimento.next_sibling

        mov_tuples = filter(None, map(parse_tr, items_do_movimento(movimento)))
        return dict(mov_tuples)


    soup = BeautifulSoup(html)

    movimentos = soup.table.findAll(attrs={"class": "tipoMovimento"})
    return [parse_movimento(m) for m in movimentos]
