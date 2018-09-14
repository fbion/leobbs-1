# Leobbs

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

## Terraform

For first run
```bash
terraform init tf
terraform apply  -auto-approve tf 

```
For second run
```bash
terraform taint null_resource.web
terraform apply  -auto-approve tf

```

## Carton

If you using Carton as perl packages management. You may want to run 
```bash
Carton install
Carton run morbo .\main.pl

```