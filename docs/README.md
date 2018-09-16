# Leobbs

Leobbs need perl >= 5.28.*

## Quick Start

You need docker and docker-compose installed.
### Prepare PostgreSQL DB

For quick create a postgres sql DB, you can run following command

```bash
docker volume create --name vol-pg -d local


docker run --restart=always --name pg \
    -e POSTGRES_PASSWORD=LeoBBS \
    -p 172.17.0.1:5432:5432 \
    -v vol-pg:/var/lib/postgresql/data \ 
    -d postgres
```

### Prepare ENV file

You should create a ENV file at your docker host  path /etc/docker/env.leobbs.env

With content:

```
DB_HOST=172.17.0.1 # Replace to your PostgresSQL DB host
DB_PORT=5432
DB_USER=postgres
DB_PW=LeoBBS
``` 
### Run
Then you can run 
```bash
docker-compose up --build

```

## Carton

**This section mostly for developer, If you are not, you may not want do this**

If you using Carton as perl packages management. You may want to run

For windows 
```bash
cpanm Carton
Carton install
Carton run morbo .\main.pl

```
For linux
```bash
cpanm Carton
carton install
carton run morbo ./main.pl

```

## Help

Any question? Welcome to add the issue 