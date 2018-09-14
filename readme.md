# Leobbs

## Quick Start

You need docker and docker-compose installed.

### Prepare ENV file

You should create a ENV file at your docker host  path /etc/docker/env.leobbs.env

With content:

```
DB_HOST=10.8.41.31 # Replace to your PostgresSQL DB host
DB_PORT=4321
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