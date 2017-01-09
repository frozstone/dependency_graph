from collections import OrderedDict
from utilities.unification import unification
from utils import Link_Types, Matching_Methods

class depgraph_heur:
    __matching_method = ''

    def __init__(self, matching_method):
        self.__matching_method = matching_method

    def __is_connected_heuristic(self, math1, math2):
        '''
            math1, math2 : lists of candidate matchers
            return True if an edge should be drawn from math1 to math2
        '''
        for idx1, mt1 in enumerate(math1):
            for idx2, mt2 in enumerate(math2):
                if mt2 != '' and (mt2 in mt1):# or (mt2.lower() in mt1.lower()): #and mt1 != mt2:
                    if idx1 == 0 and idx2 == 0 and mt2 in mt1 and math2[-1] == math1[-1]:
                        return True, Link_Types.exp
                    elif idx1 == 0 and idx2 == 0 and mt2 in mt1 and math2[-1] != math1[-1]:
                        return True, Link_Types.comp
                    elif math2[-1] == math1[-1]:
                        return True, Link_Types.simexp
                    else:
                        return True, Link_Types.simcomp
        return False, None

    def __is_connected_unification(self, math1, math2):
        unif = unification()
        for idx1, mt1 in enumerate(math1):
            for idx2, mt2 in enumerate(math2):
                isConn, link_str = unif.process(mt1, mt2)
                if isConn:
                    link = Link_Types.exp if link_str == 'exp' else Link_Types.comp
                    return True, link
        return False, None

    def create_edges(self, mts):
        '''
            mts: {gmid:[matchers]} --> unique mts
            output: edges --> {gumidparent:(gumidchild, linktype)}
        '''
        edges = OrderedDict()
        for gmid1, matchers1 in mts.iteritems():
            for gmid2, matchers2 in mts.iteritems():
                if gmid1 == gmid2: continue

                if self.__matching_method == Matching_Methods.heur:
                    is_conn, link = self.__is_connected_heuristic(matchers1, matchers2)
                elif self.__matching_method == Matching_Methods.unification:
                    is_conn, link = self.__is_connected_unification(matchers1, matchers2)

                if is_conn and gmid1 in edges:
                    edges[gmid1].append((gmid2, link))
                elif is_conn:
                    edges[gmid1] = [(gmid2, link)]
        return edges
