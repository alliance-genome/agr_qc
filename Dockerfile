FROM agrdocker/agr_python_env:latest

ARG aws_access_key_id=
ARG aws_secret_access_key=
ARG agr_version=
ARG agr_env=

ENV AWS_SECRET_ACCESS_KEY=$aws_secret_access_key \
    AWS_ACCESS_KEY_ID=$aws_access_key_id \
    AGR_VERSION=$agr_version
    AGR_ENV=$agr_env

WORKDIR /usr/src/app

ADD requirements.txt .

RUN pip3 install -r requirements.txt

ADD . .

CMD ["python3", "-u", "src/run_queries.py"]
