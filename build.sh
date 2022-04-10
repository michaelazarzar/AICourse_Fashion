#!/bin/bash
app="fashion_classification"
docker build -t ${app} .
docker run -d -p 6978:6978 \
  --name=${app} \
  -v $PWD:/app ${app}