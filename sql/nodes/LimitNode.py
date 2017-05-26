from sql.nodes.SQLNode import SQLNode
from sql.nodes.SQLNodeType import SQLNodeType

class LimitNode(SQLNode):
    """
    Requires a label. Returns 1 if label isn't valid

    limit_node = LimitNode(3)
    limit_node.to_sql()
    => LIMIT 3

    """
    def __init__(self, label, child=None, parent=None):
        label = self.word_to_int(label)

        super(LimitNode, self).__init__(SQLNodeType.LIMIT_NODE, label, "limit")

        self.add_child(child)
        self.add_parent(parent)


    @staticmethod
    def word_to_int(word):
        num_words = ['zero', 'one', 'two', 'three', 'four', 'five',
                     'six', 'seven', 'eight', 'nine', 'ten']

        several = ['some', 'few', 'several']

        try:
            limit = int(word)
        except ValueError:
            limit = 1

        if word in several:
            limit = 3

        if word in num_words:
            limit = num_words.index(word)

        return limit
