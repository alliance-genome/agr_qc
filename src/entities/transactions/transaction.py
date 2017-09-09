import time

class Transaction(object):

    def __init__(self, graph):
        self.graph = graph

    def deleteTransaction(self, query):
        result = None
        
        start = time.time()
        with self.graph.session() as session:
            with session.begin_transaction() as tx:
                result = tx.run(query)
        end = time.time()

        count = 0
        for record in result:
            print("Removed %s %s" % (record['label'], record['primaryKey']))
            count += 1

        print("Removed %s records" % (count))

        print("Processed entries in %s s" % (end - start))