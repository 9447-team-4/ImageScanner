FROM python:3

COPY . /app

RUN pip install -r /app/requirements.txt 

RUN cp /app/image-scan.py /bin/image-scan

ENTRYPOINT [ "image-scan" ]
