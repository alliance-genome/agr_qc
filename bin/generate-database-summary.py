import sys
import os
import json

from boto3.s3.transfer import S3Transfer
import boto3

import pprint
pp = pprint.PrettyPrinter(indent=4)

from dateutil.parser import parse
from datetime import datetime
from time import gmtime, strftime

from neo4j.v1 import GraphDatabase

# USAGE python bin/generate-database-report.py
#
# If files are being pushed to S3 will need to have aws cli configured
# https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html
# 
# Evironment Variables
#
# REQUIRED: $AGR_VERSION
#           $AWS_ACCESS_KEY_ID (OPTIONAL if specifying none "local" environment)
#           $AWS_SECRET_ACCESS_KEY (OPTIONAL if specifying none "local" environment)
#
# OPTIONAL: $AGR_ENV  (build, test, stage, prod)
#           If not set will default to creating local file
#           $AGR_DB_URI bolt url

bucket = "agr-db-reports"
bucketFolder = "qc-database-summary"

uri = "bolt://localhost:7687"
if "AGR_DB_URI" in os.environ:
    uri = os.environ("AGR_DB_URI")

driver = GraphDatabase.driver(uri)

if "AGR_VERSION" in os.environ:
    agrVersion = os.environ['AGR_VERSION']
else:
    print("Environment variable not set: AGR_VERSION")
    exit(1)


if "AGR_ENV" in os.environ:
    agrEnvironment = os.environ['AGR_ENV']
    print "Using environment: ", agrEnvironment
else:
    agrEnvironment = None

datetimeNow = strftime("%Y-%m-%d_%H_%M_%S", gmtime())

if agrEnvironment:
    filename = "alliance-db-summary-" + agrEnvironment + "-" + agrVersion + "-" + datetimeNow + ".json"

with driver.session() as session:
    summary = {}

    entities = {}
    with session.begin_transaction() as tx:
        for record in tx.run("""
MATCH (entity)
WITH labels(entity) AS entityTypes
RETURN count(entityTypes) AS frequency,
       entityTypes"""):
            frequency = record["frequency"]
            entityTypes = record["entityTypes"]
            if (len(entityTypes) == 1 and entityTypes[0] != "Load"):
                entities[entityTypes[0]] = frequency
            elif len(entityTypes) == 2:
                if entityTypes[1] in entities:
                    entities[entityTypes[1]][entityTypes[0]] = frequency
                else:
                    entities[entityTypes[1]] = {entityTypes[0]: frequency}
                if entityTypes[0] in entities:
                    entities[entityTypes[0]][entityTypes[1]] = frequency
                else:
                    entities[entityTypes[0]] = {entityTypes[1]: frequency}

    entityKeys = entities.keys()
    for key in entityKeys:
        if not isinstance(entities[key], int):
            if len(entities[key].keys()) == 1:
                del entities[key]

    summary = { "overview": entities }

    if agrEnvironment:
        filePath = "reports/" + filename
        with open(filePath, 'w') as f:
            print "Writing summary to file: ", filePath
            f.write(json.dumps(summary, indent=4, sort_keys=True))
        if agrEnvironment != "local":
            print "Uploading to S3 bucket: ", bucketFolder
            if "AWS_ACCESS_KEY_ID" in os.environ and "AWS_SECRET_ACCESS_KEY" in os.environ:
                 client = boto3.client('s3', aws_access_key_id = os.environ["AWS_ACCESS_KEY_ID"], aws_secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"])
                 transfer = S3Transfer(client)
                 transfer.upload_file(filePath, bucket, bucketFolder + "/" + filename)
            else:
                print "ERROR: access keys AWS_ACCESS_KEY_ID and/or AWS_SECRET_ACCESS_KEY needs to be set"
                exit(1)

        else:
            print(json.dumps(summary, indent=4, sort_keys=True))
