from lark.visitors import Interpreter

import transformer
from symbol_table import st

trans = transformer.TreeTransformer()

class GoInterpreter(Interpreter):
    def conditional(self, tree):
        conds = tree.find_data('condition')
        for cond in conds:
            trans_tree = trans.transform(cond)
            print("DEBUG: Transformed tree")
            print(trans_tree)
            if trans_tree.children[0]:
                print("DEBUG: Condition is True")
                self.visit_children(tree)

    def block_statement(self, tree):
        return trans.transform(tree)
    
    def assignment(self, tree):
        return trans.transform(tree)

    def expression(self, tree):
        return trans.transform(tree)

    def print_stmt(self, tree):
        return trans.transform(tree)
    
    def call(self, tree):
        if tree.children[0].value == 'print':
            return trans.transform(tree.children[1])