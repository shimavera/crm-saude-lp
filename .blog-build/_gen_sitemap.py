#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera o sitemap.xml a partir dos arquivos que existem de verdade.

Motivo: o sitemap era mantido à mão e o lastmod derivava. Em 07/2026 a home
declarava 2026-05-16 enquanto o arquivo tinha sido alterado em 07-08 (63 dias
de defasagem). Aqui o lastmod vem da data do último commit que tocou o arquivo,
que é a única fonte de verdade disponível.

<priority> foi removido de propósito: o Google ignora desde 2023.

Uso: python3 .blog-build/_gen_sitemap.py
"""
import os
import subprocess
import glob
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BASE = "https://lp.saudecrm.com"


def last_commit_date(path):
    """Data do último commit que tocou o arquivo. Cai para o mtime se não houver."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", path],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
        if out:
            return out
    except subprocess.CalledProcessError:
        pass
    return date.fromtimestamp(os.path.getmtime(path)).isoformat()


def url_for(path):
    """Caminho no disco -> URL pública. index.html vira o diretório."""
    rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
    if rel == "index.html":
        return BASE + "/"
    if rel.endswith("/index.html"):
        return f"{BASE}/{rel[:-len('index.html')]}"
    return f"{BASE}/{rel}"


def source_for(path):
    """
    Arquivo que representa o CONTEÚDO da página, para datar o lastmod.

    Os posts do blog são gerados a partir de _bodies/<slug>.body.html. Datar o
    .html gerado faria o lastmod pular toda vez que o template mudasse (um ajuste
    de meta tag marcaria 12 artigos como reescritos). O corpo é o que o leitor lê,
    então é ele que define se a página mudou de verdade.
    """
    rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
    if rel.startswith("blog/") and not rel.endswith("/index.html"):
        slug = os.path.basename(rel)[:-len(".html")]
        body = os.path.join(HERE, "_bodies", f"{slug}.body.html")
        if os.path.exists(body):
            return body
    return path


def main():
    paths = [os.path.join(ROOT, "index.html")]
    paths += sorted(glob.glob(os.path.join(ROOT, "blog", "*.html")))

    entries = []
    for p in paths:
        entries.append((url_for(p), last_commit_date(source_for(p))))

    # a home primeiro, depois o índice do blog, depois os posts
    def rank(e):
        u = e[0]
        if u == BASE + "/":
            return (0, u)
        if u == BASE + "/blog/":
            return (1, u)
        return (2, u)

    entries.sort(key=rank)

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url, lastmod in entries:
        lines += ["  <url>",
                  f"    <loc>{url}</loc>",
                  f"    <lastmod>{lastmod}</lastmod>",
                  "  </url>"]
    lines.append("</urlset>")

    out = os.path.join(ROOT, "sitemap.xml")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"sitemap.xml: {len(entries)} URLs")
    for url, lastmod in entries:
        print(f"  {lastmod}  {url}")


if __name__ == "__main__":
    main()
