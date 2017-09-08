from .aggregate_updater import AggregateUpdater
import os

host = os.environ['NEO4J_HOST']
port = os.environ['NEO4J_PORT']
uri = "bolt://" + host + ":" + port

if __name__ == '__main__':
	al = AggregateUpdater(uri)

	# The following order is required for testing.	
	al.runUpdates()
