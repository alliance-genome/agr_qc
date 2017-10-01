from .transaction.generic import GenericTransaction

class GenericEntities(object):
    
    def __init__(self, graph):
        self.graph = graph

    def generic_tx(self):
        tx = GenericTransaction(self.graph)
        tx.generic_tx(data)