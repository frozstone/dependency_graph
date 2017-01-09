from py2neo import Graph
from py2neo.packages.httpstream import http

class Neo4J_Mathcat:
    __conn = ''

    def __init__(self, url):
        http.socket_timeout = 9999
        self.__conn = Graph(url)

    def __escape(self, string):
        return string.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'")
   
    def __encodeUnicode(self, lst):
        newlst = []
        for ele in lst:
            newlst.append(ele.encode('utf-8'))
        return newlst

    def __joinForArray(self, lst):
        #gpid:["%s"]
        return self.__escape('","'.join(self.__encodeUnicode(lst)))

    def __joinForFulltext(self, lst):
        return self.__escape(' ### '.join(self.__encodeUnicode(lst)))

    def __create_node_statement(self, mid, doc, mathml):
        return 'CREATE (:Math {mid:"%s", doc:"%s", mathml:"%s"})' % (mid, doc, self.__escape(mathml))

    def create_nodes(self, nodes):
        '''
        nodes is {doc: {mid: mathml}} --> math expressions with attributes (gmid, gpid, gdoc, tex, context, description)
        '''
        tx = self.__conn.cypher.begin()
        batches = 10000
        cursize = 0
        for doc, maths in nodes.iteritems():
            for mid, mathml in maths.iteritems():
                tx.append(self.__create_node_statement(mid, doc, mathml))
                cursize += 1
                if cursize == batches: 
                    tx.process()
                    cursize = 0
        tx.commit()

    def __create_relationship_statement(self, midsource, midtarget, doc, heuristics):
        heuristics_text = ', '.join(['%s:"%s"' % (heur, is_used) for heur, is_used in heuristics.iteritems()])
#        return 'start source=node:node_auto_index(mid="%s", doc="%s"), target=node:node_auto_index(mid = "%s", doc="%s") CREATE (source)-[:R {%s}]->(target)' % (midsource, doc, midtarget, doc, heuristics_text)
        return 'MATCH (source:Math), (target:Math) WHERE source.mid = "%s" AND source.doc = "%s" AND target.mid = "%s" AND target.doc = "%s" CREATE (source)-[:R {%s}]->(target)' % (midsource, doc, midtarget, doc, heuristics_text)

    def create_relationships(self, relationships):
        '''
        relationships is {doc: [(source, target), ]}
        '''
        tx = self.__conn.cypher.begin()
        batches = 10000
        cursize = 0
        for doc, relations in relationships.iteritems():
            for relation, heuristics in relations.iteritems():
                midsource = relation[0]
                midtarget = relation[1]
                tx.append(self.__create_relationship_statement(midsource, midtarget, doc, heuristics))
                cursize += 1
                if cursize == batches: 
                    tx.process()
                    cursize = 0
        tx.commit()
