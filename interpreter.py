from lark.visitors import Interpreter

import transformer
from symbol_table import st

# Transfomer visits a sub-tree bottom-up and run appropriate methods
trans = transformer.TreeTransformer()

# Interpreter is used to visit the root tree top-down
class GoInterpreter(Interpreter):
    
    def program(self, tree):
        return self.visit_children(tree)


    def if_stmt(self, tree):
        trans_cond = trans.transform(tree.children[0])
        if trans_cond:
            return self.visit_children(tree.children[1])[0]
        elif len(tree.children) > 2:
            if tree.children[2].data == "block_statement":
                return self.visit_children(tree.children[2])[0]
            elif tree.children[2].data == "if_stmt":
                return self.visit(tree.children[2])


    def while_loop(self, tree):
        rel = tree.children[0]
        evs = ""
        while trans.transform(rel):
            #trans_tree = trans.transform(rel)
            blocks = tree.find_data('block_statement')
            for block in blocks:
                evl = self.visit_children(block)
                for ev in evl:
                    if ev is not None:
                        evs = evs + "\n" + str(ev)
        return evs


    def for_loop(self, tree):
        assign = tree.children[0]
        trans.transform(assign)

        rel = tree.children[1]
        ident = tree.children[2]
        evs = ""
        while trans.transform(rel):
            #trans_tree = trans.transform(rel)
            #print("DEBUG: Transformed relation")
            #print(trans_tree)
            blocks = tree.find_data('block_statement')
            for block in blocks:
                evl = self.visit_children(block)
                for ev in evl:
                    if ev is not None:
                        evs = evs + "\n" + str(ev)
            cur_value = st.get(ident)
            st.set(ident, cur_value+1)
        return evs


    def bool_logic(self, tree):
        return trans.transform(tree)

    def bool_and(self, tree):
        return trans.transform(tree)

    def bool_or(self, tree):
        return trans.transform(tree)

    def bool_not(self, tree):
        return trans.transform(tree)


    def block_statement(self, tree):
        self.visit_children(tree)


    def assignment(self, tree):
        return trans.transform(tree)

    def short_assignment(self, tree):
        return trans.transform(tree)

    def array_assignment(self, tree):
        return trans.transform(tree)


    def expression(self, tree):
        return trans.transform(tree)
    
    def printf(self, tree):
        return trans.transform(tree.children[0])
