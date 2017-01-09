from lxml import etree

class unification:
    def __occurrences(self, string, sub):
        starts = []
        start = 0
        while True:
            index = string.find(sub, start)
            start = index + 1
            if index > -1:
                starts.append(index)
            else:
                return starts

    def __unify_with_placeholder(self, mt_string, placeholder_mi, placeholder_mn):
        mt = etree.fromstring(mt_string)
        mis = mt.xpath('//mi')
        mns = mt.xpath('//mn')
       
        mi_mapping = {}
        n_mi = 0
        for mi in mis:
            if mi.text not in mi_mapping:
                n_mi += 1
                mi_mapping[mi.text] = placeholder_mi % n_mi
            mi.text = mi_mapping[mi.text]

        mn_mapping = {}
        n_mn = 0
        for mn in mns:
            if mn.text not in mn_mapping:
                #n_mn += 1
                mn_mapping[mn.text] = placeholder_mn % n_mn
            mn.text = mn_mapping[mn.text]
            
        return etree.tostring(mt)


    def __unify_with_spaces(self, mt_string, space_mi, space_mn):
        mt = etree.fromstring(mt_string)
        mis = mt.xpath('//mi')
        mns = mt.xpath('//mn')
        
        for mi in mis:
            mi.text = space_mi

        for mn in mns:
            mn.text = space_mn

        return etree.tostring(mt)
       

    def __unify(self, mt_string, width_mi, width_mn):
        mt = etree.fromstring(mt_string)

        placeholder_mi  = '%' + ('%sd' % width_mi)
        placeholder_mn  = '%' + ('%sd' % width_mn)
        space_mi        = ' ' * width_mi
        space_mn        = ' ' * width_mn
        
        if len(mt.xpath('//mo')) == 0 and len(mt.xpath('//mi') + mt.xpath('//mn')) <= 1:
            return None, None

        unification_placeholder   = self.__unify_with_placeholder(mt_string, placeholder_mi, placeholder_mn)
        unification_space         = self.__unify_with_spaces(mt_string, space_mi, space_mn)

        return unification_placeholder, unification_space

    def __remove_outermost_math_tag(self, mt_string):
        return mt_string[6:-7]

    def __preprocess(self, mt_a_string, mt_b_string):
        mt_a = etree.fromstring(mt_a_string)
        mt_b = etree.fromstring(mt_b_string)
        
        mis_a = mt_a.xpath('//mi')
        mis_b = mt_b.xpath('//mi')

        mns_a = mt_a.xpath('//mn')
        mns_b = mt_b.xpath('//mn')

        max_mis = max(len(mis_a), len(mis_b))
        max_mns = max(len(mns_a), len(mns_b))

        u_placeholder_a, u_space_a = self.__unify(mt_a_string, len(str(max_mis)), len(str(max_mns)))
        u_placeholder_b, u_space_b = self.__unify(mt_b_string, len(str(max_mis)), len(str(max_mns)))

        return u_placeholder_a, u_space_a, u_placeholder_b, u_space_b

    def __is_unification_same(self, u_placeholder_a, u_placeholder_b):
        '''
            Initial condition: u_space_a and u_space_b are same, but make sure that a can be specified from b
        '''
        mt_a = etree.fromstring('<math>%s</math>' % u_placeholder_a)
        mt_b = etree.fromstring('<math>%s</math>' % u_placeholder_b)

        mis_a = mt_a.xpath('//mi')
        mis_b = mt_b.xpath('//mi')
        mis_mapping = {}
        for mi_idx, mi in enumerate(mis_b):
            if mi.text in mis_mapping and mis_mapping[mi.text] != mis_a[mi_idx].text:
                return False
            mis_mapping[mi.text] = mis_a[mi_idx].text

        mns_a = mt_a.xpath('//mn')
        mns_b = mt_b.xpath('//mn')
        mns_mapping = {}
        for mn_idx, mn in enumerate(mns_b):
            if mn.text in mns_mapping and mns_mapping[mn.text] != mns_a[mn_idx].text:
                return False
            mns_mapping[mn.text] = mns_a[mn_idx].text

        return True

    def __is_connected(self, mt_a_string, u_placeholder_a, u_space_a, mt_b_string, u_placeholder_b, u_space_b):
        '''
            This method returns TRUE if there is an edge from A to B.
            This edge means: 1. A and B are same OR
                             2. A contains B OR
                             3. A is more specific than B, e.g. A is x + x and B is x + y
        '''
        #If either a or b is a single mi or single mn, do comparison over their original MathML without any unification
        if u_placeholder_a is None or u_placeholder_b is None:
            mt_a_string = self.__remove_outermost_math_tag(mt_a_string)
            mt_b_string = self.__remove_outermost_math_tag(mt_b_string)
            if mt_a_string == mt_b_string: return True, 'exp'
            if mt_b_string in mt_a_string: return True, 'comp'
            return False, None
        
        u_placeholder_a = self.__remove_outermost_math_tag(u_placeholder_a)
        u_placeholder_b = self.__remove_outermost_math_tag(u_placeholder_b)
        u_space_a = self.__remove_outermost_math_tag(u_space_a)
        u_space_b = self.__remove_outermost_math_tag(u_space_b)

        #To handle case #1 and #3
        if u_placeholder_a == u_placeholder_b: return True, 'exp' 
        if u_space_a == u_space_b: return self.__is_unification_same(u_placeholder_a, u_placeholder_b), 'exp'

        #To handle case #2 and #3
        b_in_a = self.__occurrences(u_space_a, u_space_b)
        for substring_start in b_in_a:
            substring = u_placeholder_a[substring_start : substring_start + len(u_placeholder_b)]
            if self.__is_unification_same(substring, u_placeholder_b): return True, 'comp'
        return False, None

    def process(self, mt_a_string, mt_b_string):
        mt_a_string = '<math>%s</math>' % mt_a_string
        mt_b_string = '<math>%s</math>' % mt_b_string
        u_placeholder_a, u_space_a, u_placeholder_b, u_space_b = self.__preprocess(mt_a_string, mt_b_string)

        return self.__is_connected(mt_a_string, u_placeholder_a, u_space_a, mt_b_string, u_placeholder_b, u_space_b)

