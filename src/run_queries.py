from aggregate_updater import AggregateUpdater
import os


if "NEO4J_HOST" in os.environ:
    host = os.environ['NEO4J_HOST']
else:
    host = "localhost"

if "NEO4J_PORT" in os.environ:
    port = int(os.environ['NEO4J_PORT'])
else:
    port = 7687

uri = "bolt://" + host + ":" + port

if __name__ == '__main__':
	al = AggregateUpdater(uri)

	# The following order is required for testing.	
	al.runUpdates()
