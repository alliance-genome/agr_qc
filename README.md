# AGR Neo4j QC Documentation

Thid repo is used for removing data in the database that does not meet the standards to be shown on the AGR web portal. These issues could arise for various reasons. Over time we intend on collecting all of the adjustments that need to be made to the database in this repository

This repo will also generating reports on the pre_QC, post_QC database and the effects of the changes on the database. The results of these tests will be made available to the AGR and lists will be sent to individual MODs / data providers. In this way we will provide feedback that can be used to make improvements to data and process used to generate the database.

## Development

First you will need a database to pull from to create the queries

```bash
docker pull agrdocker/agr_neo4j_nqc_data_image:0.6.42
```
