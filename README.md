# Notification Manager by User

## Deployed App Running on HEROKU

- [SWAGGER](https://blooming-garden-01349-26f398f01a3b.herokuapp.com/api)

### Badges

[![Github Actions](https://github.com/AndyRmCz/notification_byUser_system/actions/workflows/python-app.yml/badge.svg)](https://github.com/AndyRmCz/notification_byUser_system/actions/workflows/python-app.yml)

[![CircleCI](https://dl.circleci.com/status-badge/img/gh/AndyRmCz/notification_byUser_system/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/AndyRmCz/notification_byUser_system/tree/main)

[![Coverage Status](https://coveralls.io/repos/github/AndyRmCz/notification_byUser_system/badge.svg)](https://coveralls.io/github/AndyRmCz/notification_byUser_system)

### How to run locally coveralls

```
COVERALLS_REPO_TOKEN=XOfic96I7mC4pVcU9Yltdot9U8riRxE3Y npm run test:cov
```

### Features

- Create new Users with email and pasword
- Authenticate user and recognizes current user
- Generate user token for validation
- List User created notification
- Create and dispatch notification with channel, recipient, title and content
- Update notifications
- Delete notification

## Pre-Requisites

- Docker installed without SUDO Permission
- Docker compose installed without SUDO
- Ports free: 3000 and 5432

## How to run the APP

```
docker-compose -f docker-compose.yml up --build --force-recreate
```

## How to run the tests

```
docker-compose -f docker-compose.test.yml up --build --force-recreate
```

## Areas to improve

- Data should be moved from tests to an external file
- Generic method should be used to mock endpoints
- Error handling could be improved (I.E handle user not found)
- A Seed migration would be useful to have an already working app with data
- The ORM is being used with Synchronize instead of migrations. Migrations would be the best option
- Deployment could be done

## Errors to be fixed

- Error handling could be improved (I.E handle user not found)
- A Seed migration would be useful to have an already working app with data
- The ORM is being used with Synchronize instead of migrations. Migrations would be the best option

## Techs

- FastAPI: 0.139.0
- Python: 3.14
- SQLAlchemy: 2.0.51
- Postgres

## Decisions made

- Clean Architecture: To make project scalable and mantainable (Controller-Service-Repository-Client).
- Adapters: To translate expernal APIs responses to domain 
- SQLAlchemy: Python standard ORM, Big community and documentation
- Docker: To make portable
- PyTest: Pytest is the most used testing framework of Python.

## Route

- Local: [API Swagger](http://localhost:8000/docs#/)

## Env vars should be defined

To find an example of the values you can use .env.example