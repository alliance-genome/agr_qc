# AGR Neo4j QC Documentation

Thid repo is used for removing data in the database that does not meet the standards to be shown on the AGR web portal. These issues could arise for various reasons. Over time we intend on collecting all of the adjustments that need to be made to the database in this repository

This repo will also generating reports on the pre_QC, post_QC database and the effects of the changes on the database. The results of these tests will be made available to the AGR and lists will be sent to individual MODs / data providers. In this way we will provide feedback that can be used to make improvements to data and process used to generate the database.

## Development

These two commands will run the code with docker compose.

```bash
make startdb
make run
```

## Generating AGR reports

This script is used to generate database summary statistics. If and environment is not set it will output the json to standard out. If the envronement is set it will create a file in the reports folder. If the environment is not "local" it will also upload the report to the S3 bucket "agr-db-reports/qc-database-summary"

### Settings

See top of script for instructions: bin/generate-database-summary.py
