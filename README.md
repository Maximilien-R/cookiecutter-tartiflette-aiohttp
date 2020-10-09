# cookiecutter-tartiflette-aiohttp

A [cookiecutter](https://github.com/audreyr/cookiecutter) template for creating
a [`tartiflette`](https://github.com/tartiflette/tartiflette) AIOHTTP API.

## Contents
 
* [Features](#features)
* [Usage](#usage)
* [Deployment](#deployment)
    * [Heroku](#heroku)
* [TODO](#todo)
 
## Features

Opinionated:
* Provides a fully-featured GraphQL AIOHTTP application running with [`tartiflette`](https://github.com/tartiflette/tartiflette)
* Provides a file upload support through an implementation of the [`graphql-multipart-request-spec`](https://github.com/jaydenseric/graphql-multipart-request-spec)
* Provides `Docker` support through [`docker-compose`](https://github.com/docker/compose)
* Follows the [`gazr`](https://gazr.io) specification to launch common tasks
* Layered environment configuration system through [`dynaconf`](https://github.com/rochacbruno/dynaconf)
* Provides a configurable JSON logger through [`python-json-logger`](https://github.com/madzak/python-json-logger)
* Provides an hot reload application through [`hupper`](https://github.com/Pylons/hupper)
* Implements unit tests with [`pytest`](https://github.com/pytest-dev/pytest)
* Implements functional tests with [`pytest`](https://github.com/pytest-dev/pytest)

Optionals:
* Provides a choice of different open source licenses
* Provides `MySQL` database through [`docker-compose`](https://github.com/docker/compose)
* Provides a default [`dependabot`](https://dependabot.com) to keep your dependencies up-to-date 
* Provides implementations for health routes (`/health/ready` & `/health/live`)
* Provides a GraphiQL route (`/graphiql`)
* Provides [`Sentry`](https://sentry.io) integration
* Provides a pre-configured container deployment configuration to [`Heroku`](https://www.heroku.com) cloud provider

## Usage

Install the latest [Cookiecutter](https://github.com/audreyr/cookiecutter) if
you haven't installed it yet:
```bash
$ pip install -U cookiecutter
```

Generate your tartiflette AIOHTTP project with the following command:
```bash
$ cookiecutter https://github.com/Maximilien-R/cookiecutter-tartiflette-aiohttp.git
```

You'll be prompted for some values. Fill them to create your tartiflette
project.

Once your tartiflette AIOHTTP project created, move to your project directory:
```bash
$ cd <your-directory>
$ git init
$ git add .
$ git commit -m "Initial commit"
$ git remote add origin <your-github-repository>
$ git push -u origin master
```

Now, you can work on your project and use all of the pre-defined `Makefile`
targets (cf. [`gazr`](https://gazr.io)):
```
$ make run
$ make format
$ make style
$ make complexity
$ make security-sast
$ make test
$ make down
$ make clean
```

## Deployment

### Heroku

To deploy your project to Heroku, please, follow those simple steps:

If you haven't an Heroku account yet, please, create one [here](https://signup.heroku.com).

Then, install the `heroku` CLI to be able to deploy your project, documentation
is available [here](https://devcenter.heroku.com/articles/heroku-cli#download-and-install).

Once your Heroku account created and the `heroku` CLI installed, you can follow
thoses steps to deploy your project:
```
# Note: replace occurrences of `MY_APP` with your `project_slug` as uppercase

# Connect yourself to your Heroku account through the CLI
$ heroku login -i

# Create a new container app
$ heroku apps:create --stack container

# Adds MySQL adddon if necessary
$ heroku addons:create cleardb:ignite --version=5.7
$ heroku config:set MY_APP_database__url=$(heroku config:get CLEARDB_DATABASE_URL)

# Adds Sentry adddon if necessary
$ heroku addons:create sentry:f1
$ heroku config:set MY_APP_sentry__dsn=$(heroku config:get SENTRY_DSN)

# Push your app to Heroku
$ git push heroku master

# Open your app
$ heroku open

# Shutdown your app
$ heroku ps:scale web=0

# Destroy your app
$ heroku apps:destroy
```

## TODO

* Add an option to use `PostgreSQL` instead of `MySQL`
* Add an option to handle GraphQL subscriptions
* Setup some CI configuration (Travis-CI, GitHub Actions...)
* Add an option to have APM
* Add an option to have statsd
