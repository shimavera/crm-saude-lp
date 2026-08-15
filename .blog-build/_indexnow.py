#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Avisa Bing/Copilot (e demais buscadores do consórcio IndexNow) que as URLs
do sitemap mudaram. Rodar DEPOIS do deploy, nunca antes: o buscador vai
buscar a página no ato, e se o conteúdo antigo ainda estiver no ar o aviso
se perde.

Isso importa para IA: o ChatGPT search usa o índice do Bing.

Uso:
    python3 .blog-build/_indexnow.py            # envia todas as URLs do sitemap
    python3 .blog-build/_indexnow.py <url> ...  # envia só as URLs indicadas
"""
import os, sys, re, json, glob, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
HOST = "saudecrm.com"
ENDPOINT = "https://api.indexnow.org/indexnow"


def key_from_disk():
    """A chave é o nome do arquivo <chave>.txt na raiz, servido publicamente."""
    for p in glob.glob(os.path.join(ROOT, "*.txt")):
        nome = os.path.basename(p)[:-4]
        if re.fullmatch(r"[0-9a-f]{32,128}", nome):
            return nome
    raise SystemExit("Nenhum arquivo de chave IndexNow (<hex>.txt) na raiz do projeto.")


def urls_do_sitemap():
    xml = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
    return re.findall(r"<loc>(.*?)</loc>", xml)


def main():
    key = key_from_disk()
    urls = sys.argv[1:] or urls_do_sitemap()
    payload = {
        "host": HOST,
        "key": key,
        "keyLocation": f"https://{HOST}/{key}.txt",
        "urlList": urls,
    }
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        # 200 = aceito, 202 = aceito e a chave será validada depois
        print(f"IndexNow {r.status}: {len(urls)} URLs enviadas")
        for u in urls:
            print(f"  {u}")


if __name__ == "__main__":
    main()
