REG := 100225593120.dkr.ecr.us-east-1.amazonaws.com

registry-docker-login:
ifneq ($(shell echo ${REG} | egrep "ecr\..+\.amazonaws\.com"),)
	@$(eval DOCKER_LOGIN_CMD=aws)
ifneq (${AWS_PROFILE},)
	@$(eval DOCKER_LOGIN_CMD=${DOCKER_LOGIN_CMD} --profile ${AWS_PROFILE})
endif
	@$(eval DOCKER_LOGIN_CMD=${DOCKER_LOGIN_CMD} ecr get-login-password | docker login -u AWS --password-stdin https://${REG})
	${DOCKER_LOGIN_CMD}
endif

build: registry-docker-login
	docker build -t ${REG}/agr_qc_run:develop --build-arg REG=${REG} .

startdb:
	REG=${REG} docker-compose up -d neo4j.qc

execdb: startdb
	docker exec -ti neo4j.qc bin/cypher-shell

removedb:
	docker-compose down -v

run: build
	REG=${REG} docker-compose up agr_qc

bash:
	REG=${REG} docker-compose up agr_qc bash

updatedb: registry-docker-login
	REG=${REG} docker-compose up -d neo4j.qc
	docker-compose down -v
	REG=${REG} docker-compose up -d neo4j.qc
	sleep 10
	docker build -t ${REG}/agr_qc_run:latest --build-arg REG=${REG} .
	REG=${REG} docker-compose up agr_qc

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
		-t ${REG}/agr_qc_run:develop \
		/bin/bash -c "python3 bin/generate-database-summary.py"

