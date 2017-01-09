from lxml import etree, objectify
from StringIO import StringIO
from utils import fence_pair, Splitter_Symbols

class norm_splitter:
    __fpair = fence_pair()
    __dtd = ''
    __xml_parser = etree.XMLParser()
    __relation_symbols = set([])

    def __init__(self, dtd, relation_fl):
        self.__dtd = dtd
        self.__xml_parser = etree.XMLParser(load_dtd = True, dtd_validation = True)
        self.__fpair = fence_pair()

        ss = Splitter_Symbols(relation_fl)
        self.__relation_symbols = ss.relation_symbols

    def __process(self, tree_string):
        '''
            Input   : string of an original MathML
            Output  : string of left side subexpression
        '''
        tree = etree.parse(StringIO(self.__dtd + tree_string), self.__xml_parser).getroot()
        objectify.deannotate(tree, cleanup_namespaces = True)
        stack_fences = []
        for child in tree:
            #A subexpression is skipped
            if not child.text and (len(child) > 0 and child[0].text and child[0].text not in self.__fpair.fences_open and child[0].text not in self.__fpair.fences_close): continue

            if child.text and child.text in self.__fpair.fences_open: 
                stack_fences.append(child.text)
                continue
            if len(child) > 0 and child[0].text and child[0].text in self.__fpair.fences_open:
                stack_fences.append(child[0].text)
                continue

            #Pop an open fence if it pairs with the close
            if child.text and child.text in self.__fpair.fences_close and self.__fpair.ispair_fence_open_close(stack_fences[-1], child.text): 
                stack_fences.pop()
                continue
            if len(child) > 0 and child[0].text and child[0].text in self.__fpair.fences_close and self.__fpair.ispair_fence_open_close(stack_fences[-1], child[0].text):
                stack_fences.pop()
                continue
                
            #We get the splitting position!!!
            if ((child.text and child.text in self.__relation_symbols) or (len(child) > 0 and child[0].text and child[0].text in self.__relation_symbols)) and len(stack_fences) == 0:
                #Remove the next siblings
                for sibling in child.itersiblings():
                    tree.remove(sibling)
                tree.remove(child)
                return etree.tostring(tree)
        #By default (no splitter), return the input
        return tree_string

    def split(self, tree_string):
        try:
            result_tree_string = self.__process(tree_string)
            if result_tree_string != tree_string: return result_tree_string
        except:
            #the splitting fails (usually because the expression is a subexpression of an eqnarray)
            return None
        return None
