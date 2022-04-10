FROM ubuntu


RUN \
 apt-get -y update && \
 apt-get -y install software-properties-common && \
 apt-get -y update && \
 apt-get install -y python3-dev && \
 apt-get install -y python3-pip


WORKDIR /app
RUN pip install --upgrade pip
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt


Add Server.py /app
COPY templates /app/templates
COPY models /app/models

RUN mkdir -p / app/Upload


EXPOSE 6978 6978

CMD ["python3", "Server.py"]

# build command:
# bash build.sh

# run command
# docker run fashion_classification