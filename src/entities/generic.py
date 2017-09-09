from .transactions.transaction import Transaction

class GenericEntities(object):
    def __init__(self, graph):
        Transaction.__init__(self, graph)

    def generic_tx(self):

        #Removes skeleton nodes
        #query = """
        #   MATCH (n)
        #   WHERE size(keys(n))=1
        #   DETACH DELETE (n)
        #"""
        #Transaction.deleteTransaction(self, query)

        # remove all nodes that do not have any edges
        query = """
            MATCH (n)
            WHERE size((n)--())=0
            WITH n, COLLECT(DISTINCT labels(n)) AS label, n.primaryKey AS primaryKey
            DELETE (n)
            RETURN label, primaryKey
        """
        Transaction.deleteTransaction(self, query)