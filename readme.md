# Leobbs

## Quick Start

You need docker and docker-compose installed.

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