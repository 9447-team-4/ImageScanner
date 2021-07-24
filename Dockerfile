FROM python:3

RUN apt-get update && \
    apt-get install -y wget && \
    apt-get clean && \
    wget https://github.com/snyk/snyk/releases/download/v1.666.0/snyk-linux -O snyk && \
    chmod a+x snyk && \
    cp snyk /usr/bin/


COPY . /app

RUN pip install -r /app/requirements.txt 

RUN cp /app/*.py /bin/

ENTRYPOINT [ "gitea-reporter.py" ]
