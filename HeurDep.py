from time import time
from os import listdir, path
from lxml import etree, objectify
from pickle import load
from sys import argv
from StringIO import StringIO
from collections import OrderedDict

from utilities.norm_arxiv       import norm_arxiv
from utilities.norm_attribute   import norm_attribute
from utilities.norm_mrow        import norm_mrow
from utilities.norm_outer_fence import norm_outer_fence
from utilities.norm_splitter    import norm_splitter
from utilities.norm_tag         import norm_tag

from utilities.utils            import Link_Types, Matching_Methods, utils
from utilities.depgraph_heur    import depgraph_heur

__dtd = '<!DOCTYPE math SYSTEM "resources/xhtml-math11-f.dtd">'
__xmlns = ' xmlns="http://www.w3.org/1998/Math/MathML"'
__relation_fl = 'resources/math_symbols_unicode.dump'
__xml_parser = etree.XMLParser(remove_blank_text = True, load_dtd = True, resolve_entities = True)


def __get_clean_mathml(mt_string):
    mt_tree = etree.parse(StringIO(__dtd + mt_string), __xml_parser).getroot()
    objectify.deannotate(mt_tree, cleanup_namespaces=True)
    return mt_tree

def __extract_math_line_arxiv(line):
    cells = line.strip().split('\t')
    latexml_id  = cells[0]
    para_id     = cells[1]
    kmcs_id     = cells[2]
    gmid        = '#'.join([para_id, kmcs_id, latexml_id])

    mt_string = '\t'.join(cells[3:]).replace(__xmlns, "")
    mt = __get_clean_mathml(mt_string)
    return gmid, mt

def __extract_math_line_acl(line):
    cells = line.strip().split('\t')
    gmid  = cells[0]

    mt_string = '\t'.join(cells[1:]).replace(__xmlns, "")
    mt = __get_clean_mathml(mt_string)
    return gmid, mt


def __write_edges(edges, toflname):
    lns = []
    for gmid, nodes in edges.iteritems():
        lns.append( '\t'.join([gmid, ' '.join([node[0] for node in nodes])]) + '\n')
    f = open(toflname, 'w')
    f.writelines(lns)
    f.close()

def __get_dep_graph(math_dir, dep_dir, fl, matching_method):
    '''
    input: file from math_new
    output: 
        1. edges: {gumid1:[(gumid2, linktype)]} --> component list
        2. gumidmappings: {gmid:gumid}
    '''
    #useful utilities classes
    n_arxiv         = norm_arxiv()
    n_attribute     = norm_attribute()
    n_mrow          = norm_mrow(__dtd)
    n_outer_fence   = norm_outer_fence()
    n_tag           = norm_tag(__dtd)
    n_splitter      = norm_splitter(__dtd, __relation_fl)
    u               = utils()
    depgraph        = depgraph_heur(matching_method)

    lns = open(path.join(math_dir, fl)).readlines()

    #enumerate if there is no id in the <math> tag
    rawmts = OrderedDict()
    mts = OrderedDict()
        
    #for xhtml, enumerate mathtag; for xml, enumerate expressiontag; for math_new, enumerate the lines
    for ln in lns:
        if ln.strip() == '': continue
        gmid, mt = __extract_math_line_acl(ln)

        rawmts[gmid] = mt

        #replace <m:math> with <math>
        mt_string_initial = n_arxiv.remove_math_prefix(etree.tostring(mt))

        #remove annotation, attributes, and finally get rid the <math> tag
        mt_string_formatted = n_arxiv.remove_annotation(etree.parse(StringIO(__dtd + mt_string_initial)).getroot())
        mt_string_formatted = n_attribute.normalize(mt_string_formatted)

        #normalize mrow
        mt_string_formatted = n_mrow.normalize(mt_string_formatted) 

        #remove fences
        mt_string_formatted = etree.tostring(n_outer_fence.remove_outer_fence(etree.parse(StringIO(__dtd + mt_string_formatted)).getroot()))[6:-7]

        #expand maths (normalize tags and/or case)
        expanded = n_tag.normalize_tags('<math>%s</math>' % mt_string_formatted)
        #expanded = [n_mrow.normalize('<math>%s</math>' % exp) for exp in expanded]

        if len(expanded) > 0:
            expanded[-1] = n_mrow.normalize('<math>%s</math>' % expanded[-1])[6:-7]
            expanded.extend([etree.tostring(n_outer_fence.remove_outer_fence(etree.parse(StringIO(__dtd + '<math>%s</math>' % exp)).getroot()))[6:-7] for exp in expanded])
        else:
            expanded = [mt_string_formatted]

        mts[gmid] = [expanded[0]]

        #split around the equality and get the left side subexpressions
        left_subexp = n_splitter.split('<math>%s</math>' % expanded[-1])
        if left_subexp is None: continue

        left_subexp = n_mrow.normalize(left_subexp)[6:-7]
        if not u.is_empty_tag(left_subexp):
            expanded_left = n_tag.normalize_tags(left_subexp)
            #expanded_left = [n_mrow.normalize('<math>%s</math>' % exp)[6:-7] for exp in expanded_left]

            mts[gmid].append(left_subexp)
            mts[gmid].extend(expanded_left)
        mts[gmid] = list(set(mts[gmid]))
    edges = depgraph.create_edges(mts)
    __write_edges(edges, path.join(dep_dir, fl))


if __name__ == '__main__':
    #Preparation
    math_path   = argv[1]
    dep_dir     = argv[2]
    math_dir    = path.dirname(math_path) #path to math_new directory
    math_fl     = path.basename(math_path) #./1/0704.0097.txt
    __get_dep_graph(math_dir, dep_dir, math_fl, Matching_Methods.heur)
