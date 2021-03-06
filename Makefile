REG := 100225593120.dkr.ecr.us-east-1.amazonaws.com
DOCKER_PULL_TAG := latest
DOCKER_BUILD_TAG := latest

registry-docker-login:
ifneq ($(shell echo ${REG} | egrep "ecr\..+\.amazonaws\.com"),)
	@$(eval DOCKER_LOGIN_CMD=docker run --rm -it -v ~/.aws:/root/.aws amazon/aws-cli)
ifneq (${AWS_PROFILE},)
	@$(eval DOCKER_LOGIN_CMD=${DOCKER_LOGIN_CMD} --profile ${AWS_PROFILE})
endif
	@$(eval DOCKER_LOGIN_CMD=${DOCKER_LOGIN_CMD} ecr get-login-password | docker login -u AWS --password-stdin https://${REG})
	${DOCKER_LOGIN_CMD}
endif

build: registry-docker-login
	docker build -t ${REG}/agr_qc_run:develop --build-arg REG=${REG} .

#TODO: Remove all use of docker image `agr_neo4j_qc_data_image`.
#      That means all use of the docker-compose service neo4j.qc is potentially to be deprecated as well,
#      which means most this Makefile is currently non-functional and to be redefined.

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
	docker build -t ${REG}/agr_qc_run:${DOCKER_BUILD_TAG} --build-arg REG=${REG} --build-arg DOCKER_PULL_TAG=${DOCKER_PULL_TAG} .
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

