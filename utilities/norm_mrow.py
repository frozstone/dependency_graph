from lxml import etree, html, objectify
from norm_attribute import norm_attribute
from StringIO import StringIO
import sys

class norm_mrow:
    __dtd = ''
    __xml_parser = etree.XMLParser()

    def __init__(self, dtd):
        self.__dtd      = dtd
        self.__xml_parser   = etree.XMLParser(load_dtd = True, dtd_validation = True, resolve_entities = True)

    def __parse_with_dtd(self, mt_string):
        return etree.parse(StringIO(self.__dtd + mt_string), self.__xml_parser).getroot()

    def __parse_as_html(self, mt_string):
        return html.fromstring(mt_string)

    def __is_valid(self, mt_string):
        try:
            self.__parse_with_dtd(mt_string)
            return True
        except:
            return False

    def __parse_mt_and_get_mrow(self, mt_string):
        mt_tree = self.__parse_as_html(mt_string)
        mt_mrows = mt_tree.xpath('.//mrow[not(@other)]')
        return mt_tree, mt_mrows

    def __remove_mrow(self, mt_string):
        mt_tree, mt_mrows           = self.__parse_mt_and_get_mrow(mt_string)
        temp_mt_tree, temp_mt_mrows = self.__parse_mt_and_get_mrow(mt_string)

        while len(mt_mrows) > 0:
            for mrowd_id, mrow in enumerate(mt_mrows):
                if len(mrow.xpath('.//mrow[not(@other)]')) > 0: continue

                #remove mrow only if it contains no other mrow and it does not violate the dtd
                temp_mt_mrows[mrowd_id].drop_tag()
                if self.__is_valid(etree.tostring(temp_mt_tree)): 
                    mrow.drop_tag()
                    continue

                #if the new mathml is not valid, recover the temp_mt_tree, and set the attribute 'is_checked' in the corresponding mrow in mt_tree
                temp_mt_tree, temp_mt_mrows = self.__parse_mt_and_get_mrow(mt_string)
                mrow.attrib['other'] = 'True'

            mt_string = etree.tostring(mt_tree)
            mt_tree, mt_mrows           = self.__parse_mt_and_get_mrow(mt_string)
            temp_mt_tree, temp_mt_mrows = self.__parse_mt_and_get_mrow(mt_string)
        return mt_string

    def __remove_attributes(self, mt_string):
        na = norm_attribute()
        return na.normalize(mt_string)

    def normalize(self, mt_string):
        result_string = self.__remove_mrow(mt_string)
        result_string = self.__remove_attributes(result_string)
        return result_string

