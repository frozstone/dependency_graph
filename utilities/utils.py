from enum import Enum
from pickle import load
from lxml import etree

class Link_Types(Enum):
    comp    = 1
    simcomp = 2 
    exp     = 3
    simexp  = 4


class Matching_Methods(Enum):
    heur        = 1
    unification = 2


class Splitter_Symbols():
    __relation_fl = ''
    relation_symbols = set([])

    def __init__(self, relation_fl):
        self.__relation_fl = relation_fl
        self.__load_relation_symbols()

    def __load_relation_symbols(self):
        f = open(self.__relation_fl, 'rb')
        self.relation_symbols = load(f)
        f.close()

class fence_pair:
    fences_open   = '([{'
    fences_close  = ')]}'

    def ispair_fence_open_close(self, fopen, fclose):
        return self.fences_open.index(fopen) == self.fences_close.index(fclose)

class utils:
    def is_empty_tag(self, mt_string):
        mt_tree = etree.fromstring('<math>%s</math>' % mt_string)
        etree.strip_tags(mt_tree, '*')
        return mt_tree.text == None or mt_tree.text == ''
