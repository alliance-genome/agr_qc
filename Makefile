build:
	docker build -t agrdocker/agr_qc_run:develop .

startdb:
	docker-compose up -d neo4j.qc

execdb: startdb
	docker exec -ti neo4j.qc bin/cypher-shell

removedb:
	docker-compose down -v

run: build
	docker-compose up agr_qc

bash:
	docker-compose up agr_qc bash

updatedb:
	docker-compose up -d neo4j.qc
	docker-compose down -v
	docker-compose up -d neo4j.qc
	sleep 10
	docker build -t agrdocker/agr_qc_run:latest .
	docker-compose up agr_qc

.PHONY: create-db-summary
create-db-summary: $(call print-help,run,"Run the application in docker")
	docker run \
		--name db-summary \
		--network my-network \
		-e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
		-e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
		-e AGR_VERSION=${AGR_VERSION} \
		-e AGR_ENV=${AGR_ENV} \
		-e AGR_DB_URI=${AGR_DB_URI} \
		-t agrdocker/agr_qc_run:develop \
		/bin/bash -c "python3 bin/generate-database-summary.py"

