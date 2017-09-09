import time

class Transaction(object):

    def __init__(self, graph):
        self.graph = graph

    def deleteTransaction(self, query):
        result = None
        start = time.time()
        with self.graph.session() as session:
            # with session.begin_transaction() as tx:
            result = session.run(query)
        end = time.time()

        for record in result:
            print("%s %s" % (record['label'], record['primaryKey']))

        print("Processed entries in %s s" % (end - start))