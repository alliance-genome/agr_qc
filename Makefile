build:
	docker build -t agrdocker/agr_qc_run:develop .

startdb:
	docker-compose up -d neo4j.qc

execdb: startdb
	docker exec -ti neo4j.qc bin/cypher-shell

pull:
	docker pull agrdocker/agr_neo4j_nqc_data_image:develop

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
