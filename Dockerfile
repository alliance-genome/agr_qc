ARG REG=agrdocker
ARG DOCKER_IMAGE_TAG=latest

FROM ${REG}/agr_base_linux_env:${DOCKER_IMAGE_TAG}

ENV AWS_SECRET_ACCESS_KEY=\
    AWS_ACCESS_KEY_ID= \
    AGR_VERSION= \
    AGR_ENV= \
    AGR_DB_URI=

WORKDIR /usr/src/app

ADD requirements.txt .

RUN pip3 install -r requirements.txt

ADD . .

RUN ["chmod", "+x", "/usr/src/app/bin/generate-database-summary.py"]

CMD ["python3", "-u", "src/run_queries.py"]
