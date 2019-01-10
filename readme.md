# Leobbs

leobbs previous was built with perl , now we rewrite it with kotlin + spring boot

## Quick Start

You need docker and docker-compose installed.
### Prepare MariaDB


For quick create a MariaDB sql DB, you can run following command. 

(And you may still use mysql, it's ok)

```bash
docker volume create mydata
docker run --restart=always --name mydb -p 3306:3306 -v mydata:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=admin@123 -d mariadb:10.4 --character-set-server=utf8mb4 --collation-server=utf8mb4_general_ci

```

### Run
Then you can run 
```bash
docker-compose up --build

```
