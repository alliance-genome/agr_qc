import time

class Transaction(object):

	def __init__(self, graph):
		self.graph = graph

	def deleteTransaction(self, query):
		start = time.time()
		with self.graph.session() as session:
			with session.begin_transaction() as tx:
				tx.run(query)
		end = time.time()
		print("Processed entries in %s s" % (end - start))
