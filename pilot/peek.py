#!/usr/bin/env python3
"""Print the first rows of the largest table in a supplementary file, for hand-checking classifications.
Usage: peek.py PMCID filename [nrows]"""
import sys, zipfile, io, os, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import openpyxl
pmc, fn = sys.argv[1], sys.argv[2]; n = int(sys.argv[3]) if len(sys.argv) > 3 else 6
z = zipfile.ZipFile(os.path.join(os.environ.get("PILOT_DATA","data"), "zips", pmc + ".zip"))
name = next(x for x in z.namelist() if os.path.basename(x) == fn); b = z.read(name); ext = os.path.splitext(fn.lower())[1]
def show(rows, label):
    rows = [r for r in rows if any(c not in (None, "") for c in r)]
    print(f"--- {label}: {len(rows)} rows x {max((len(r) for r in rows), default=0)} cols")
    for r in rows[:n]: print("   ", [str(c)[:18] for c in r[:8]])
if ext in (".xlsx", ".xlsm"):
    wb = openpyxl.load_workbook(io.BytesIO(b), read_only=True, data_only=True)
    for ws in wb.worksheets[:4]: show([r for _, r in zip(range(5000), ws.iter_rows(values_only=True))], ws.title)
elif ext == ".xls":
    import xlrd; wb = xlrd.open_workbook(file_contents=b)
    for ws in wb.sheets()[:4]: show([ws.row_values(i) for i in range(min(ws.nrows, 5000))], ws.name)
elif ext == ".docx":
    import docx; d = docx.Document(io.BytesIO(b))
    for k, t in enumerate(d.tables[:4]): show([[c.text for c in r.cells] for r in t.rows], f"table{k+1}")
elif ext == ".pdf":
    import pdfplumber, logging; logging.getLogger("pdfminer").setLevel(logging.ERROR)
    with pdfplumber.open(io.BytesIO(b)) as pdf:
        print(f"[pdf {len(pdf.pages)} pages] first text: {(pdf.pages[0].extract_text() or '')[:160]!r}")
        k=0
        for i,pg in enumerate(pdf.pages[:30]):
            for tb in pg.extract_tables() or []:
                k+=1
                if k<=3: show(tb, f"page{i+1} table{k}")
        print(f"   total tables in first 30 pages: {k}")
else:
    t = b[:2_000_000].decode("utf-8", "replace"); d = "\t" if t.count("\t") > t.count(",") else ","
    show(list(csv.reader(io.StringIO(t), delimiter=d)), "text")
