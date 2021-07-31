FROM docker:git

RUN apk update && \
    apk add --no-cache wget python3 python3-dev musl-dev libstdc++ py3-pip gcc && \
    wget https://github.com/snyk/snyk/releases/download/v1.671.0/snyk-alpine -O snyk && \
	chmod a+x snyk && \
    cp snyk /bin/


COPY . /app

RUN pip install -r /app/requirements.txt --ignore-installed six

RUN cp /app/*.py /bin/

ENTRYPOINT [ "gitea-reporter.py" ]
