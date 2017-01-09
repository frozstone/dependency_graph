from norm_mrow import norm_mrow

if __name__ == '__main__':
    dtd = '<!DOCTYPE math SYSTEM "../resources/xhtml-math11-f.dtd">'
    n = norm_mrow(dtd)
    assert(n.normalize('<math><mrow><mn>3</mn></mrow><mo>+</mo><mrow><mi>i</mi></mrow></math>') == '<math><mn>3</mn><mo>+</mo><mi>i</mi></math>')
    assert(n.normalize('<math><msub><mi>x</mi><mrow><mn>2</mn></mrow></msub></math>') == '<math><msub><mi>x</mi><mn>2</mn></msub></math>')
    assert(n.normalize('<math><msub><mi>x</mi><mrow><mn>2</mn><mo>+</mo><mi>k</mi></mrow></msub></math>') == '<math><msub><mi>x</mi><mrow><mn>2</mn><mo>+</mo><mi>k</mi></mrow></msub></math>')
    assert(n.normalize('<math><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn><mo>+</mo><mi>k</mi></mrow></msub></math>') == '<math><msub><mi>x</mi><mrow><mn>2</mn><mo>+</mo><mi>k</mi></mrow></msub></math>')
    assert(n.normalize('<math><msub><mrow><mi>x</mi><mo>*</mo><mi>y</mi></mrow><mrow><mn>2</mn><mo>+</mo><mi>k</mi></mrow></msub></math>') == '<math><msub><mrow><mi>x</mi><mo>*</mo><mi>y</mi></mrow><mrow><mn>2</mn><mo>+</mo><mi>k</mi></mrow></msub></math>')
    assert(n.normalize('<math><msub><mrow><mi>x</mi><mo>*</mo><mrow><mi>y</mi></mrow></mrow><mrow><mn>2</mn><mo>+</mo><mi>k</mi></mrow></msub></math>') == '<math><msub><mrow><mi>x</mi><mo>*</mo><mi>y</mi></mrow><mrow><mn>2</mn><mo>+</mo><mi>k</mi></mrow></msub></math>')
