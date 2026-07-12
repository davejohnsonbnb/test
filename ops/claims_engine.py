import zipfile, re
from xml.etree import ElementTree as ET

M = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'

def load_styles(z):
    """style index -> fill rgb hex (or None)"""
    styles = ET.fromstring(z.read('xl/styles.xml'))
    fills = []
    for f in styles.find(M+'fills'):
        pf = f.find(M+'patternFill')
        rgb = None
        if pf is not None:
            fg = pf.find(M+'fgColor')
            if fg is not None:
                rgb = fg.get('rgb')
        fills.append(rgb)
    xfs = []
    cellxfs = styles.find(M+'cellXfs')
    for xf in cellxfs:
        xfs.append(int(xf.get('fillId') or 0))
    return [fills[i] if i < len(fills) else None for i in xfs]

def classify(rgb):
    if not rgb or len(rgb) < 6: return None
    h = rgb[-6:]
    r,g,b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    if r>235 and g>235 and b>235: return None          # white
    if abs(r-g)<15 and abs(g-b)<15: return None        # gray
    if b < min(r,g)-50 and abs(r-g) < 60: return 'yellow'
    if g > r+20 and g >= b+20: return 'green'
    if r > g+20 and r > b+20: return 'red'
    return f'other:{h}'

def load_shared(z):
    ss=[]
    try:
        root = ET.fromstring(z.read('xl/sharedStrings.xml'))
        for si in root.findall(M+'si'):
            ss.append(''.join(t.text or '' for t in si.iter(M+'t')))
    except KeyError: pass
    return ss

def sheet_rows(z, n, styles, ss):
    """yield (rownum, {col: (text, colorclass)})"""
    root = ET.fromstring(z.read(f'xl/worksheets/sheet{n}.xml'))
    for row in root.iter(M+'row'):
        vals={}
        for c in row.iter(M+'c'):
            ref=c.get('r'); col=re.match(r'([A-Z]+)',ref).group(1)
            t=c.get('t'); v=c.find(M+'v'); s=c.get('s')
            txt = (ss[int(v.text)] if t=='s' else v.text) if v is not None else ''
            color = classify(styles[int(s)]) if s is not None else None
            vals[col]=(txt or '', color)
        if any(v[0].strip() for v in vals.values()):
            yield int(row.get('r')), vals

def excel_date(serial):
    from datetime import date, timedelta
    try:
        return (date(1899,12,30)+timedelta(days=float(serial))).isoformat()
    except (ValueError, TypeError):
        return str(serial)

def analyze(path):
    z = zipfile.ZipFile(path)
    styles = load_styles(z); ss = load_shared(z)
    wb = z.read('xl/workbook.xml').decode('utf-8')
    tabs = re.findall(r'<sheet[^>]*name="([^"]+)"[^>]*/?>', wb)
    out = {}
    for i, tab in enumerate(tabs, 1):
        try:
            rows = list(sheet_rows(z, i, styles, ss))
        except KeyError:
            continue
        out[tab] = rows
    return out

def row_color(vals):
    counts={}
    for txt,color in vals.values():
        if color: counts[color]=counts.get(color,0)+1
    if not counts: return None
    return max(counts, key=counts.get)
