from lxml import etree, objectify

class norm_attribute:
    def __remove_attributes_node(self, mt_node):
        if not mt_node.attrib: return True
        for at in mt_node.attrib.keys():
            del mt_node.attrib[at]

    def __remove_attributes_tree(self, mt_tree):
        self.__remove_attributes_node(mt_tree)
        for child in mt_tree:
            self.__remove_attributes_tree(child)

    def normalize(self, mt_string):
        mt_tree = etree.fromstring(mt_string)
        self.__remove_attributes_tree(mt_tree)
        objectify.deannotate(mt_tree, cleanup_namespaces=True)
        return etree.tostring(mt_tree)

