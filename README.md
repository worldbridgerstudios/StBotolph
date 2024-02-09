# Election Night

This project provides a Django web app for processing & presenting election results on election night.

It consists of:

* A Django project `election_night`
* A Django app `election_results`
* Django Rest Framework REST APIs.
* A `Dockerfile` and `docker-compose.yml` to build & run the app containerised in Docker.
* A `.gitlab-ci.yml` for automated build-test of the Docker container in Gitlab CI pipelines.

## How it works

### Frontend

The frontend is built using HTML 5, Bootstrap 4, jQuery and Vue JS.

Currently it is just a single template-rendered home page, accessible at the root url.

> The Vue SFC Loader is used to allow use of Vue components without requiring Node.js

### Upload Election Results

The `/api/upload/` endpoint can be used to upload an election results file in CSV format.

> An example file can be found at [election_results/test_data/spec-data.csv](election_results/test_data/spec-data.csv).

You can use Postman or `curl` to test, e.g. when running locally (host `127.0.0.1`):

```bash
curl -X POST -F "file=@election_results/test_data/spec-data.csv" "http://127.0.0.1:8000/api/upload/any-file-name.csv/"
```

### View Constituency Information

The `/api/constituencies/` endpoint summarises constituencies and party votes.

### View Party Information

The `/api/parties/` endpoint provides a mapping of party codes and names.

### View Party Total Results

The `/api/total-results/` endpoint provides party "total results", like MP count and total vote count across constituencies.

## Developer Guide

### Quickstart

* Clone the git repo and `cd` to the working directory
* Create a virtual environment with `python3 -m venv .`
* Activate virtual environment with `. bin/activate`.
* Install requirements with `pip install -r requirements.txt`
* Run `./manage.py migrate` to apply migrations (this generates `db.sqlite3`)
* Run `./manage.py test` to run unit tests
* Run `curl` command linked in _Upload Election Results_ above to populate with example data.
* Run `./manage.py runserver` then access in a web browser or via `curl`
* Run `./manage.py collectstatic -c --no-input` to overwrite all static files (`static/`).

> Example URLs for local web browsing:
> 
> * http://127.0.0.1:8000/api/constituencies/
> * http://127.0.0.1:8000/api/constituencies/1/
> * http://127.0.0.1:8000/api/parties/
> * http://127.0.0.1:8000/api/parties/1/
> * http://127.0.0.1:8000/api/total-results/
> * http://127.0.0.1:8000/api/total-results/4/

### Django Models

* `Constituency` - Represents a voter constituency.
* `Party` - Represents a political party.
* `PartyVoteCount` - Represents a vote count specific to a particular constituency and party.

### Dockerfile

The `Dockerfile` (currently minimal) does the following:

* Installs the Django project & app to `/app/`
* This includes the SQLite db file, prepopulated with initial party data _(see below)_.

The `docker-compose.yml` does the followwing:

* Defines a `web` service for the Docker image.
* Runs the dockerised Django app using `./manage.py runserver`.
* Exposes port `8000` as used by `runserver`.
* Mounts the current working directory ('.') into `/app/` for live development and debugging.

To build the Docker image from Dockerfile, use `docker compose build`.
> The resulting image name is `docker.io/library/nick-brown-web`.

To run the Docker container, use `docker compose up` (with `-d` after to detach).
> When running locally, accessing using localhost address `127.0.0.1`.

To run unit tests in the Docker container, use:

```bash
docker run docker.io/library/nick-brown-web /app/manage.py test
```

### Gitlab CI Configuration

The `.gitlab-ci.yml` currently defines:

* A `build` stage & job to build the Docker container.
* A `test` stage & job to run all unit tests within the Docker container.

### Party Data

The initial party data is stored in a migration, thus is installed by `./manage.py migrate`.

Currently this consists of:

| Code | Party name          |
|------|---------------------|
| C    | Conservative Party  |
| G    | Green Party         |
| Ind  | Independent         |
| L    | Labour Party        |
| LD   | Liberal Democrats   |
| SNP  | SNP                 |
| UKIP | UKIP                |

---

## Original Project Spec

It's election night and we have a feed of election results from a data supplier. They will supply us a file which will be updated throughout the night as results come in.

## What you have
### Input file
The fields in the file will be separated by commas but each row will vary in length as described below.
A result will consist of:
1. A constituency
2. A repeating set of pairs with the party code and the votes cast

So for example:

    Cardiff West, 11014, C, 17803, L, 4923, UKIP, 2069, LD
    Islington South & Finsbury, 22547, L, 9389, C, 4829, LD, 3375, UKIP, 3371, G, 309, Ind

> **_NOTE:_** Constituency names containing a comma will be escaped as with '\\,'

### Updates
New results files will be arriving all night, and the application needs to process them. These files will include updates or new results for some constituencies. The previous results generated by the service may be behind the actual results or may contain an error. We want to be able to combine the existing results with new updated results files. If a constituency has an entry for a party in the new results file, corresponding values should be overridden in the existing results data. If the constituency is not present in the existing results data the result should be added entirely from the new file.


## What we want
### Import the raw file
An API (and optionally a UI) to be used by the supplier to upload the results files. 

###  RESTful API
We need two RESTful APIs:

#### Constituency API
* shows the constituency name
* translates the party code into a full name (see mapping, below) 
* shows the total number of votes for each party
* shows the share of the vote as a percentage of all the votes cast
* shows who is winning the constituency

#### Total Results API
* shows number of total MPs per party
* shows number of total votes per party

### UI
We also want a UI that:
* Shows, per constituency, constituency data from the Constituency API.
* Shows how the parliament seats are distributed over parties, as in https://members.parliament.uk/parties/Commons. The design of the UI does NOT need to be the same as the example. This page needs to use the Constituency API and the Total Results API

### Packaging
The application should be packaged in a Docker container and should run locally using docker compose.

### CI
The CI jobs in the repo should include as a minimum the building of the container.

## Appendix
### Party codes
| Code | Party name          |
|------|---------------------|
| C    | Conservative Party  |
| L    | Labour Party        |
| UKIP | UKIP                |
| LD   | Liberal Democrats   |
| G    | Green Party         |
| Ind  | Independent         |
| SNP  | SNP                 |
