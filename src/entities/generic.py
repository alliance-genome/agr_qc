from .transaction import Transaction

class GenericTransactions(object):
	def __init__(self, graph):
		Transaction.__init__(self, graph)

	def generic_tx(self):
		'''
		Removes skeleton GO nodes
		'''

		query = """
			MATCH (n)
            WHERE size(keys(n))<1
            DELETE (n)
		"""

        # removese all nodes that do not have any edges
        query2 = """
			MATCH (n)
			WHERE size((n)--())=0
			DELETE (n)
		"""
		Transaction.query_transaction(self, query)
