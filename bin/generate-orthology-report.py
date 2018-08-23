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

    orthology_file.write( "Gene1ID\tGene1Symbol\tGene1SpeciesTaxonID\tGene1SpeciesName\tGene2ID\tGene2Symbol\tGene1SpeciesTaxonID\tGene1SpeciesName\tAlgorithms\tAlgorithmsMatch\tOutOfAlgorithms\tIsBestScore\tIsBestRevScore\n")
 
    orthologList = set()

    with session.begin_transaction() as tx:
        for record in tx.run("""MATCH (species1)<-[sa:FROM_SPECIES]-(gene1:Gene)-[o:ORTHOLOGOUS]->(gene2:Gene)-[sa2:FROM_SPECIES]->(species2:Species)
WHERE o.strictFilter
OPTIONAL MATCH (algorithm:OrthoAlgorithm)-[m:MATCHED]-(ogj:OrthologyGeneJoin)-[association:ASSOCIATION]-(gene1)
WHERE ogj.primaryKey = o.primaryKey
OPTIONAL MATCH (algorithm2:OrthoAlgorithm)-[m2:NOT_MATCHED]-(ogj2:OrthologyGeneJoin)-[ASSOCIATION]-(gene1)
WHERE ogj2.primaryKey = o.primaryKey
RETURN gene1.primaryKey AS gene1ID,
       gene1.symbol AS gene1Symbol,
       gene2.primaryKey AS gene2ID,
       gene2.symbol AS gene2Symbol,
       collect(DISTINCT algorithm.name) as Algorithms,
       count(DISTINCT algorithm.name) AS numAlgorithmMatch,
       count(DISTINCT algorithm2.name) AS numAlgorithmNotMatched,
       toString(o.isBestScore) AS best,
       toString(o.isBestRevScore) AS bestRev,
       species1.primaryKey AS species1TaxonID,
       species1.name AS species1Name,
       species2.primaryKey AS species2TaxonID,
       species2.name AS species2Name"""):
            algorithms = "|".join(set(record["Algorithms"]))
            numAlgorithm = record["numAlgorithmMatch"] + record["numAlgorithmNotMatched"]
            orthology_file.write("\t".join([record["gene1ID"],
                                            record["gene1Symbol"],
                                            record["species1TaxonID"],
                                            record["species1Name"],
                                            record["gene2ID"],
                                            record["gene2Symbol"],
                                            record["species2TaxonID"],
                                            record["species2Name"],
                                            algorithms,
                                            str(record["numAlgorithmMatch"]),
                                            str(numAlgorithm),
                                            record["best"],
                                            record["bestRev"]]) + "\n")

    orthology_file.close()
