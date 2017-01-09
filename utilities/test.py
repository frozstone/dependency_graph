from norm_mrow import norm_mrow
from lxml import etree

dtd = '<!DOCTYPE math SYSTEM "../resources/xhtml-math11-f.dtd">'
x = '<math><mrow><msub><mi>Z</mi><mrow><mi>&#955;</mi><mo>,</mo><mi>&#956;</mi></mrow></msub><mo>=</mo><mrow><mo>dim</mo><mo>&#8289;</mo><mrow><mi>Hom</mi><mo>&#8290;</mo><mrow><mo>(</mo><mrow><msubsup><mi>&#945;</mi><mi>&#955;</mi><mo>+</mo></msubsup><mo>,</mo><msubsup><mi>&#945;</mi><mi>&#956;</mi><mo>-</mo></msubsup></mrow><mo>)</mo></mrow></mrow></mrow></mrow></math>'
#x = '<math><mrow><msub><mi>Z</mi><mrow><mi>&#955;</mi></mrow></msub><mo>=</mo><mrow><mo>dim</mo><mo>&#8289;</mo><mrow><mi>Hom</mi><mo>&#8290;</mo><mrow><mo>(</mo><mrow><msubsup><mi>&#945;</mi><mi>&#955;</mi><mo>+</mo></msubsup><mo>,</mo><msubsup><mi>&#945;</mi><mi>&#956;</mi><mo>-</mo></msubsup></mrow><mo>)</mo></mrow></mrow></mrow></mrow></math>'
print etree.tostring(etree.fromstring(x), pretty_print=True)
nm = norm_mrow(dtd)
print nm.normalize(x)
