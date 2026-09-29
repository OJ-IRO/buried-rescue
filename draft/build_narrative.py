#!/usr/bin/env python3
"""Rebuild narrative.html (and Narrative.pdf) from essay-v5.md, keeping the page-1 figure and styles."""
import re, subprocess, markdown, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
md = open("essay-v5.md").read()
html = open("narrative.html").read()
fig = re.search(r'<div class="fig">.*?\n</div>', html, re.S).group(0)
body = md[md.index("**In brief.**"):]
h = markdown.markdown(body, extensions=["tables"])
h = re.sub(r"<h2>(Prompt \d): ([^<]+)</h2>", r'<h2><span class="eyebrow">\1</span>\2</h2>', h)
h = h.replace("<h2>Use of Generative AI</h2>", '<h2><span class="eyebrow">Disclosure</span>Use of Generative AI</h2>').replace("<!--FIG-->", fig)
head_end = html.index("</div>", html.index('class="head"')) + 6
open("narrative.html", "w").write(html[:head_end] + "\n" + h + "</body></html>")
chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=8000",
                f"--print-to-pdf={os.path.abspath('Narrative.pdf')}", "file://" + os.path.abspath("narrative.html")], capture_output=True)
import pdfplumber, logging; logging.disable(logging.WARNING)
with pdfplumber.open("Narrative.pdf") as p:
    t = "\n".join(pg.extract_text() or "" for pg in p.pages)
    print(f"Narrative.pdf: {len(p.pages)} pages, {len(t[t.find('In brief'):].split())} words from 'In brief'")
