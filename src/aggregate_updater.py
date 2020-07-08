from entities import *
from entities.transactions import *
import time
from neo4j import GraphDatabase

class AggregateUpdater(object):
	def __init__(self, uri):
		self.graph = GraphDatabase.driver(uri, auth=("neo4j", "neo4j"))

	def runUpdates(self):
		entity = GenericEntities(self.graph)
		entity.generic_tx()
