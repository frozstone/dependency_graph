from lxml import etree
from StringIO import StringIO
from pickle import dump

dtd = '<!DOCTYPE math SYSTEM "xhtml-math11-f.dtd">'
parser = etree.XMLParser(load_dtd = True, resolve_entities = True)

def latex2unicode(latex_symbol):
    mathml_entity = '<mo>%s;</mo>' % latex_symbol.replace('\\', '&').lower()
    doc = etree.parse(StringIO(dtd + mathml_entity), parser).getroot()
    return doc.text

lns = open('math_symbols_latex.txt').readlines()
results = set(['=', ':'])
for ln in lns:
    cells = ln.strip().split()
    for cell in cells[1:]:
        if cell == 'or': continue
        try:
            results.add(latex2unicode(cell))
        except:
            print '%s undefined' % cell

f = open('math_symbols_unicode.dump', 'wb')
dump(results, f)
f.close()
