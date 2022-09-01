# use python as base image
FROM python:3.7-alpine

RUN apk add --no-cache mariadb-dev

# working directory
WORKDIR /app

# add documents to working directory
ADD . /app


# install requirements
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# open port 8050
EXPOSE 5000

# set environment name
ENV NAME OpentoAll

# run app
CMD ["python", "app.py"]