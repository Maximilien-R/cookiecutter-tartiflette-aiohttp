# cookiecutter-tartiflette-aiohttp

A [cookiecutter](https://github.com/audreyr/cookiecutter) template for creating
a [`tartiflette`](https://github.com/tartiflette/tartiflette) AIOHTTP API.

## Contents
 
* [Features](#features)
* [Usage](#usage)
* [TODO](#todo)
 
## Features

* [`gazr`](https://gazr.io) specification
* Unit testing with [`pytest`](https://github.com/pytest-dev/pytest)
* Functional testing with [`pytest`](https://github.com/pytest-dev/pytest)
* Docker support using [`docker-compose`](https://github.com/docker/compose) for development
* Optional MySQL database
* Configuration through `.yml` files and  environment variables with
[`dynaconf`](https://github.com/rochacbruno/dynaconf)

## Usage

Install the latest [Cookiecutter](https://github.com/audreyr/cookiecutter) if
you haven't installed it yet:
```
$ pip install -U cookiecutter
```

Generate a tartiflette AIOHTTP project with the following command:
```
$ cookiecutter https://github.com/Maximilien-R/cookiecutter-tartiflette-aiohttp.git
```

You'll be prompted for some values. Fill them to create your tartiflette
project.

Once your tartiflette AIOHTTP project created, move to your project directory:
```
$ cd <your-directory>
$ git init
$ git add .
$ git commit -m "Initial commit"
$ git remote add origin <your-github-repository>
$ git push -u origin master
```

Now, you can work on your project and use all of the pre-defined `Makefile`
targets:
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

## TODO

* Add an option to use `PostgreSQL` instead of `MySQL`
* Setup some CI configuration (Travis-CI, GitHub Actions...)
* Add an option to setup a GraphiQL route
* Add an option to handle GraphQL subscriptions
