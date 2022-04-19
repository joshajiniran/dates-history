# A Dates Fun Fact API

An API that generates fun facts around historical dates. Built with FastAPI and Postgresql DB and Deployed on Heroku

## Description

The API manages historical fun facts by using month and day parameters to fetch them and display for users

## Getting Started

### Dependencies

The API was tested on Linux Ubuntu 20.04 and Python 3.9.4.

- docker and docker-compose
- Python 3.8+
- FastAPI
- Other dependencies are in the requirements.txt and are installed during the build

### Building the app

- You will need to export both PORT and DATABASE_URL into the shell environment before building the docker image.

On Linux

```
export DATABASE_URL=postgresql:<postgres_user>:<postgres_pswd>@<postgres_host>/<db_name>
export PORT=8000

docker-compose up -d --build or docker-compose up --build
```

To run the migration, although this would be executed automatically from script upon build.
You need to ensure the database <db_name> has been created by visiting [Adminer](http://localhost:8080)

- Ensure you run the command at the root of the project.

```
docker exec -it api alembic upgrade head
```

### Testing the app

Upon successful build you can view the API documentation at [API Doc](http://localhost:8000) or the redoc version at [API Redoc](http://localhost:8000/documentation).

There is a deployed version on [Heroku](https://dates-facts-api.herokuapp.com)

You can test the API locally using pytest but ensure the test db has been created before running this command.

Use the command below to test using pytest.

```
docker exec -it api pytest
```

## Help

If you encounter any problem while building, kindly reach out through issues on [GitHub](https://github.com/joshajiniran/dates-api.git)

## Authors

Contributors names and contact info

Joshua Ajiniran

## Version History

This is inital release

- 0.1.1 (coming)
  - Build API on async
  - Use SQLModel ORM for database operations.
- 0.1.0
  - Initial Release
