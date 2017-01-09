import re
from lxml import etree
from StringIO import StringIO

from utils import utils 

class norm_tag:
    __tags_with_base = ['mroot', 'msub', 'msup', 'msubsup', 'munder', 'mover', 'munderover', 'mmultiscripts'] #have not considered mstyle
    __re_base_tags = '<(tags)>((?!(tags)>).)*</(tags)>'

    __dtd = ''

    def __init__(self, dtd):
        self.__dtd = dtd
        self.__generate_regex()

    def __generate_regex(self):
        tags = '|'.join(self.__tags_with_base)
        self.__re_base_tags = self.__re_base_tags.replace('tags', tags)

    def __get_value_of_math_tag(self, mt_string):
        return mt_string.replace('<math>', '').replace('</math>', '')

    def __expand_maths(self, mt_string):
        '''
            mts * {idx:'<math>'}
            Remember to remove <math> tags
        '''
        tag = re.search(self.__re_base_tags, mt_string)
        if tag is None:
            #no new matcher candidate
            return [self.__get_value_of_math_tag(mt_string)]
        
        nonbase = etree.parse(StringIO(self.__dtd + mt_string[tag.start():tag.end()].encode('utf-8'))).getroot()
        base = etree.tostring(nonbase[0])
        new_mt_string = mt_string[:tag.start()] + base + mt_string[tag.end():]

        try:
            #check if we can get deeper
            return [self.__get_value_of_math_tag(mt_string)] + self.__expand_maths(new_mt_string)
        except:
            print 'stack overflow'
            return [self.__get_value_of_math_tag(mt_string)]

    def normalize_tags(self, mt_string):
        expanded = self.__expand_maths(mt_string)
        u = utils()
        return [exp for exp in expanded if not u.is_empty_tag(exp)]

