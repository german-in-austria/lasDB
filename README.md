## lasDB

### 1. Start a PostgreSQL container
like this:
`docker run --name my-postgres -e POSTGRES_PASSWORD=passwort -e POSTGRES_USER=user -e POSTGRES_DB=personendb postgres`

Use ` -p 5432:5432` to expose a port for easy access through a GUI like pgAdmin.

### 2. Start the "lasDB" App with a container-link and an exposed port
`docker run -p 3333:80 --env-file=.env --link my-postgres:postgres lasDB/lasDB:stage`

### 3. Setup the App/Database
run these commands from inside the container:
 - `python3.5 /home/docker/code/app/manage.py makemigrations`
 - `python3.5 /home/docker/code/app/manage.py migrate auth`
 - `python3.5 /home/docker/code/app/manage.py migrate`
 - `python3.5 /home/docker/code/app/manage.py createsuperuser`


#### Environment Variables
If none of these are specified, it will fall back to an internal SQLite DB.
Put these into a `.env` file for convenient access.

| Variable              | Example                                  |
|-----------------------|------------------------------------------|
| LAS_DB                | `django.db.backends.postgresql_psycopg2` |
| LAS_DB_NAME           | `lasdb`                                  |
| LAS_DB_USER           | `user`                                   |
| LAS_DB_PASSWORD       | `passwort`                               |
| LAS_DB_PORT           | `5432`                                   |
| LAS_DB_HOST           | `postgres`                               |
| LAS_STATIC_ROOT       | `/static`                                |


### Sonstiges
 - `/admin/` Admin

### Backup
```
sudo docker exec $(sudo docker ps -q --filter name=r-las-db-lasdb-1) pg_dump -U lasdbuser lasdb > lasdb-2020-08-31.sql 2>lasdb-2020-08-31_sql.err
```