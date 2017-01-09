from lxml import etree

class norm_arxiv:

    def remove_math_prefix(self, mt_string):
        return mt_string.replace('<m:', '<').replace('</m:', '</')

    def remove_annotation(self, mt):
        '''
            mt: an xml element
            TODO:
                1. Remove the latex and MathML Content annotations
                2. Remove the semantics tag if any
                3. Remove the 'mstyle' tag
        '''
        #remove annotation and annotation-xml
        for ann in mt.findall('.//annotation') + mt.findall('.//annotation-xml'):
            ann.getparent().remove(ann)

        #Remove the semantics tag if any
        etree.strip_tags(mt, 'semantics')

        #Remove the mstyle tags
        etree.strip_tags(mt, 'mstyle')

        return etree.tostring(mt)
