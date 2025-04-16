
## Setup

> After cloning the repo:


### (1) install dependencies

> $ pip install -r requirements.txt


#### (2) create a .env file


- Add the following to your env file:

```env

# Cloudflare R2 config (this is optional: you can reconfigure the settings.py to upload files in the /media dir for dev purposes)
TOKEN_VALUE=...
ACCESS_KEY_ID=...
SECRET_ACCESS_KEY=...
ENDPOINT=...


# MAILJET CONFIG (this is optional: if you want to be able to delete account and change email/password)
MAILJET_API_KEY=...
MAILJET_SECRET_KEY=...


# Django Config
DEBUG=True # for dev purposes
ALLOWED_HOSTS=* 
SECRET_KEY=... # secret key




# Database
DATABASE_URL=postgresql://... # the postgresql db url


# CORS
ALLOWED_ORIGINS=...


```



### (2) create the compose.yml file (for the postgresql db and admin)

> Note: if this is too complicated for you, you can just leave the DATABASE_URL empty; django will default to the .sqlite3 db.


```yml

services:
  db:
    container_name: voidback_pgsql
    image: postgres
    restart: always


    environment:
      POSTGRES_USER: voidbackAdmin # keep or replace this
      POSTGRES_PASSWORD: passwd # replace this
      POSTGRES_DB: voidback


    ports:
      - 5432:5432


    volumes:
      - pgdata


    networks:
      - voidbackNet



  pgadmin:
    container_name: voidback_pgadmin
    image: dpage/pgadmin4
    restart: always

    environment:
      PGADMIN_DEFAULT_EMAIL: example@gmail.com # replace this
      PGADMIN_DEFAULT_PASSWORD: example_password # replace this


    ports:
      - 5050:80



    volumes:
      - pgadmin_data

    networks:
      - voidbackNet



volumes:
  pgdata:
    driver: local
    driver_opts:
      type: 'none'
      o: bind
      device: /media/pibox/4TB/volumes/pgdata # replace this with the path you wish to store pgdata


  pgadmin_data:
    driver: local
    driver_opts:
      type: 'none'
      o: bind
      device: /media/pibox/4TB/volumes/pgadmin_data # replace this with the path you wish to store pgadmin_data



networks:
  voidbackNet: # voidbackNet is shared between postgresql and pgadmin
```



> lastly: spin up the docker compose and add the appropriate urls to the .env file of the django backend, and run it.


