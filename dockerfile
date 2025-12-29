# FROM python:3.8 
# # FROM python:onbuild

# # apt-get mysql-client

# # RUN apt-get update \
# # 	&& apt-get install --no-install-recommends \
# # 		postgresql-client \
# # 	&& rm -rf /var/lib/apt/lists/*

# COPY ./ /app
# WORKDIR /usr/src/app

# # COPY requirements.txt ./
# # RUN pip install --upgrade pip
# RUN pip install --upgrade pip

# RUN pip install -r requirements.txt

# EXPOSE 8000/tcp
# EXPOSE 8000/udp

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


FROM python:3.8.5-alpine

WORKDIR /usr/src/app
COPY . .

# RUN apk add --no-cache mariadb-connector-c-dev
RUN apk add mariadb-connector-c-dev
RUN apk update && apk add python3 python3-dev mariadb-dev build-base && pip3 install mysqlclient && apk del python3-dev mariadb-dev build-base

RUN apk add gcc musl-dev \
    && apk add libffi-dev openssl-dev cargo
RUN apk add netcat-openbsd

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

# RUN django-admin startproject dbtest