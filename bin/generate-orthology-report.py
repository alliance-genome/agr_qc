import sys

from neo4j.v1 import GraphDatabase

# USAGE python bin/generateorthology-report.py <output-file>

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri)

outputFile = sys.argv[1]

with driver.session() as session:

    orthology_file = open(outputFile,'w')

    orthology_file.write( "gene1\tgene2\talgorithms\talgorithmsMatch\toutOfAlgorithms\tisBestScore\tisBestRevScore\n")
 
    with session.begin_transaction() as tx:
        for record in tx.run("""MATCH (gene1:Gene)-[o:ORTHOLOGOUS]->(gene2:Gene)
                                WHERE gene1.taxonId = "NCBITaxon:9606"
                                      AND (o.isBestScore = True OR o.isBestRevScore = True)
                                WITH gene1, gene2, o
                                MATCH (algorithm:OrthoAlgorithm)-[m:MATCHED]-(ogj:OrthologyGeneJoin)-[association:ASSOCIATION]-(gene1)
                                WITH algorithm, ogj, gene1, gene2, o,count(DISTINCT algorithm.name) as numAlgorithm
                                WHERE ogj.primaryKey = o.primaryKey
                                      AND numAlgorithm >= 3
                                      OR algorithm.name = "ZFIN"
                                      OR algorithm.name = "HGNC"
                                      OR (numAlgorithm = 2 AND o.isBestScore = True and o.isBestRevScore = True)
                                OPTIONAL MATCH (algorithm2:OrthoAlgorithm)-[m2:MATCHED]-(ogj2:OrthologyGeneJoin)-[association2:ASSOCIATION]-(gene1)
                                WHERE ogj2.primaryKey = o.primaryKey
                                OPTIONAL MATCH (algorithm3:OrthoAlgorithm)-[]-(ogj3:OrthologyGeneJoin)-[ASSOCIATION]-(gene1)
                                WHERE ogj3.primaryKey = o.primaryKey
                                RETURN gene1.modGlobalId as Gene1,gene2.modGlobalId as Gene2, collect(algorithm2.name) as algorithms,count(DISTINCT algorithm2.name) as numAlgorithmMatch, count(DISTINCT algorithm3) as numAlgorithm, toString(o.isBestScore) as best,toString(o.isBestRevScore) as bestRev"""):
            algorithms = "|".join(set(record["algorithms"]))
            numAlgorithmMatch = str(record["numAlgorithmMatch"])
            numAlgorithm = str(record["numAlgorithm"])
            gene1 = record["Gene1"]
            gene2 = record["Gene2"]
            best = record["best"]
            bestRev = record["bestRev"]
            orthology_file.write("\t".join([gene1,gene2,algorithms,numAlgorithmMatch,numAlgorithm,best,bestRev]) + "\n")

    orthology_file.close()
