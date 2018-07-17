import sys

from dateutil.parser import parse
from datetime import datetime
from time import gmtime, strftime

from neo4j.v1 import GraphDatabase

# USAGE python bin/generateorthology-report.py <output-file>

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri)

outputFile = sys.argv[1]
databaseVersion = sys.argv[2]

with driver.session() as session:

    orthology_file = open(outputFile,'w')

    datetimeNow = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    
    header = """#########################################################################
#
# Ortholog File
# Source: Alliance of Genomic Resources (Alliance)
# Filter: stringent
# Filter Details:
#   Ortholog needs to be called by at least 3 Algorithms
#        or is being called by either ZFIN or HGNC algorithms
#        and either is best score or is best reverse score
#   or ortholog is called by 2 algorithms and is either best score or best reverse score
# Datebase Version: {databaseVersion}
# Date: {datetimeNow}
#
#########################################################################
""".format(datetimeNow = datetimeNow, databaseVersion=databaseVersion)

    orthology_file.write(header)
   
#                                     AND gene2.modGlobalId = "FB:FBgn0036980"
#                                      gene1.taxonId = "NCBITaxon:9606"

    orthology_file.write( "Gene1ID\tGene1Symbol\tGene2ID\tGene2Symbol\tAlgorithms\tAlgorithmsMatch\tOutOfAlgorithms\tIsBestScore\tIsBestRevScore\n")
 
    orthologList = set()

    with session.begin_transaction() as tx:
        for record in tx.run("""MATCH (gene1:Gene)-[o:ORTHOLOGOUS]->(gene2:Gene)
                                WHERE (o.isBestScore = True OR o.isBestRevScore = True)
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
                                OPTIONAL MATCH (algorithm3:OrthoAlgorithm)-[m3:NOT_CALLED]-(ogj3:OrthologyGeneJoin)-[ASSOCIATION]-(gene1)
                                WHERE ogj3.primaryKey = o.primaryKey
                                RETURN gene1.primaryKey AS gene1ID,
                                       gene1.symbol AS gene1Symbol,
                                       gene2.primaryKey AS gene2ID,
                                       gene2.symbol AS gene2Symbol,
                                       collect(algorithm2.name) as algorithms,
                                       count(DISTINCT algorithm2.name) as numAlgorithmMatch,
                                       count(DISTINCT algorithm3.name) as numAlgorithmNotCalled,
                                       toString(o.isBestScore) as best,
                                       toString(o.isBestRevScore) as bestRev"""):
            algorithms = "|".join(set(record["algorithms"]))
            numAlgorithmMatch = str(record["numAlgorithmMatch"])
            numAlgorithm = 12 - record["numAlgorithmNotCalled"]
            numAlgorithm = str(numAlgorithm)
            best = record["best"]
            bestRev = record["bestRev"]
            matchStr = record["gene2ID"] + "-" + record["gene1ID"]

            if matchStr in orthologList: continue
            
            revMatchStr = record["gene1ID"] + "-" + record["gene2ID"] 
            orthologList.add(revMatchStr)

            orthology_file.write("\t".join([record["gene1ID"],
                                            record["gene1Symbol"],
                                            record["gene2ID"],
                                            record["gene2Symbol"],
                                            algorithms,
                                            numAlgorithmMatch,
                                            numAlgorithm,
                                            best,
                                            bestRev]) + "\n")

    orthology_file.close()
