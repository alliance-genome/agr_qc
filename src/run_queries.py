from aggregate_updater import AggregateUpdater
import os

useTestObject = os.environ['TEST_SET']
if useTestObject == "True":
    useTestObject = True # Convert string to boolean. TODO a better method?

host = os.environ['NEO4J_HOST']
port = os.environ['NEO4J_PORT']
uri = "bolt://" + host + ":" + port

if __name__ == '__main__':
    al = AggregateLoader(uri, useTestObject)

    # The following order is required for testing.	
    al.runUpdates()
