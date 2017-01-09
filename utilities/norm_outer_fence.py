from lxml import etree
from utils import fence_pair

class norm_outer_fence:
    __fpair = fence_pair()

    def __is_outer_fence(self, tree):
        stack_fences = []
        start_fence = ''
        if len(tree) == 0 or not tree[0].text or tree[0].text not in self.__fpair.fences_open:
            return False
        for child in tree:
            if len(stack_fences) == 2 and stack_fences[-1] in self.__fpair.fences_close:
                return False
            
            if not child.text and (len(child) > 0 and child[0].text and child[0].text not in self.__fpair.fences_open and child[0].text not in self.__fpair.fences_close): continue

            if child.text and child.text in self.__fpair.fences_open and start_fence == '':
                stack_fences.append(child.text)
                first_fence = child.text
                continue
            '''
            if len(child) > 0 and child[0].text and child[0].text in self.__fpair.fences_open and start_fence == '':
                stack_fences.append(child[0].text)
                first_fence = child[0].text
                continue
            '''

            if child.text and  child.text in self.__fpair.fences_close and self.__fpair.ispair_fence_open_close(stack_fences[-1], child.text) and len(stack_fences) > 1:
                stack_fences.pop()
                continue
            '''
            if len(child) > 0 and child[0].text and child[0].text in self.__fpair.fences_close and self.__fpair.ispair_fence_open_close(stack_fences[-1], child[0].text) and len(stack_fences) > 1:
                stack_fences.pop()
                continue
            '''

            if child.text and child.text in self.__fpair.fences_close and self.__fpair.ispair_fence_open_close(stack_fences[-1], child.text):
                stack_fences.append(child.text)
                continue
            '''
            if len(child) > 0 and child[0].text and child[0].text in self.__fpair.fences_close and self.__fpair.ispair_fence_open_close(stack_fences[-1], child[0].text):
                stack_fences.append(child[0].text)
                continue
            '''
        return len(stack_fences) == 2 and stack_fences[-1] in self.__fpair.fences_close

    def remove_outer_fence(self, tree):
        if self.__is_outer_fence(tree):
            tree.remove(tree[-1])
            tree.remove(tree[0])
            return self.remove_outer_fence(tree)

        if len(tree) == 1 and tree[0].tag == 'mfence':
            #skip the outer mrow or mfence
            tree[0].tag = 'math'
            return self.remove_outer_fence(tree[0])

        return tree

