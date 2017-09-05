import time

class Transaction(object):

    def __init__(self, graph):
		self.graph = graph

	def queryTransaction(self, query):
		start = time.time()
		with self.graph.session() as session:
			with session.begin_transaction() as tx:
				tx.run(query, data=data)
		end = time.time()
		print("Processed %s entries. %s r/s" % (len(data), round((len(data) / (end - start)),2) ))
