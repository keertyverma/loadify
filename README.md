# Loadify

[Loadify](https://loadify.herokuapp.com/) is a product importer tool. This is built as example project to showcase Django ecosystem. This app is made live at [https://loadify.herokuapp.com/](https://loadify.herokuapp.com/) Primary skills required for complete development of this tool are:

1. Knowledge about following tools
   1. Django + Postgres
   2. SSE - Server Side events
   3. Celery + RabbitMQ
2. Skills
   1. Ability to handle long running processes
   2. Use ORMs and deployment

This project is designed in such a way that it can scale easily and doesn't block resources by running on single thread.

We need to be able to import products from a CSV file and into our SQL database. Given there are half a million products to be imported into the database, we need this to be done on a pretty UI that we can use.

## Toolkit

The tools are:

1. Web framework: Django
2. Asynchronous execution: Celery with RabbitMQ
3. ORM: Django
4. Database: Postgres
5. Deployment: Heroku

## What is implemented

### STORY 1

As a user, I am able to upload a large CSV file of 500K products to the app. If there are existing duplicates, we overwrite the data. Deduplication is done using the SKU of the product. SKU is case
insensitive. Though not in the CSV file, some products are active and others should be inactive. The SKU is expected to be unique.

### STORY 1A

When the user is uploading, the user is displayed a live stream of what is happening. We are using [SSE](https://github.com/fanout/django-eventstream) to implement this.

### STORY 2

After I upload the file, I am able to view all of the products, search and filter them. This is on a URL like `/products`. This view should also has a filter to see just the active products and inactive products.

### STORY 3

As a user, it is possible to delete all existing records and start a fresh upload.

### STORY 4

As a user, we are able to add/update product manually from UI.

### STORY 5

As a user, we are able to configure multiple webhooks which should be triggered when product is created and updated manually from UI(not from csv import).

Note: Design is scalable and would not impact application performance.

## What is remaining

1. Deployment on Heroku is causing following problems
   1. I am uploading file to local storage for now due to cost reasons. Heroku `worker` process is not able to detect file uploading using `web` process
   2. ASGI server for SSE events is not working on live deployment. I am getting 404 on that endpoint.
2. Unit test cases in project
3. Handle file uploads taking longer than 30 seconds

## Running locally

1. Ensure that you have installed all the dependencies by running the following commands:

   ```bash
   pip install -r requirements.txt
   ```

2. Start a Postgres instance. This can be done by running the [official Docker image of Postgres](https://hub.docker.com/_/postgres).

   ```bash
   mkdir -p ~/dummy/postgres_12
   docker pull postgres:12.2
   docker run --name mypostgres -p 5432:5432 -v ~/dummy/postgres_12:/var/lib/postgresql/data -e POSTGRES_PASSWORD=mysecretpwd -d postgres:12.2
   ```

   Now login into Postgres using your favorite client or you can use docker image for the same

   ```bash
   docker exec -it mypostgres bash
   psql -U postgres
   ```

   When logged in create a database using command

   ```SQL
   CREATE DATABASE loadify;
   ```

3. Update the Postgres connection details and other mandatory configs by exporting an environment variable with following command

   ```bash
    export DATABASE_URL='postgres://postgres:mysecretpwd@127.0.0.1:5432/loadify'
    export DJANGO_SETTINGS_MODULE='settings.base'
    export DJANGO_SERVER_URL='http://localhost:8000/'
   ```

   I prefer using [direnv](https://direnv.net/) for this.

4. Run following command to start the server. This will start the server in a continuously running process

   ```bash
   python manage.py migrate --settings=settings.base
   python manage.py runserver --settings=settings.base
   ```

   We are using custom settings override by specifying a new file using `--settings` argument.

5. To start the Celery workers, start a RabbitMQ instance using [official image at Docker](https://hub.docker.com/_/rabbitmq) by running the following command

   ```bash
   docker pull rabbitmq:3
   docker run -d -p 5672:5672 --hostname my-rabbit --name rabbit-mq rabbitmq:3
   ```

6. Start the worker by running the following command

   ```bash
   celery worker -A loadify -l info
   ```

   This will start the instance and set the log level at `INFO`.

7. Navigate to URL [http://localhost:8000](http://localhost:8000) and start using the app.

## Deployment

1. This project is deployed with the help of `Heroku` at [https://loadify.herokuapp.com/](https://loadify.herokuapp.com/).

2. We are using Postgres provided by [Heroku-Postgres](https://www.heroku.com/postgres) and RabbitMQ provided by [CloudAMQP](https://www.cloudamqp.com/).

3. Follow the guidelines mentioned [at heroku documentation](https://devcenter.heroku.com/articles/celery-heroku) to deploy a Django + Celery app on Heroku. `Procfile` at the root of folder is used to denote all the processed to be run.

4. Update the following config vars, which are passed to your processes as environment variables

   ```bash
   SECRET_KEY='<Django secret key to handle CSRF>'
   BROKER_URL='Rabbit MQ connection string'
   DATABASE_URL='Postgres connection string'
   ALLOWED_HOSTS='Host of your Heroku deployment e.g. loadify.herokuapp.com'
   DJANGO_SERVER_URL='Host of your Heroku deployment e.g. https://loadify.herokuapp.com/'
   DJANGO_SETTINGS_MODULE='settings.production'
   DISABLE_COLLECTSTATIC=1
   ```

   `DATABASE_URL` will be added automatically if you use `Heroku-Postgres`

5. Navigate to URL provided by Heroku and start using your app.
