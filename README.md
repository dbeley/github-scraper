# github-scraper

## Requirements

- pandas
- pygithub
- tqdm
- working config.ini (see config_sample.ini for an example)

## Installation of the virtualenv (recommended)

```
pipenv install
```

## Usage


### repos_information_by_user

```
python repos_information_by_user.py -h
pipenv run python repos_information_by_user.py -h
```

```
usage: repos_information_by_user.py [-h] [--debug] [-u USER] [-f FILE]

Repos information by user

optional arguments:
  -h, --help            show this help message and exit
  --debug               Display debugging information
  -u USER, --user USER  Users to search (separated by comma)
  -f FILE, --file FILE  File containing the users (one by line)
```

### starred_repos

```
python starred_repos.py -h
pipenv run python starred_repos.py -h
```

```
usage: starred_repos.py [-h] [--debug] [-u USER]

Get github starred repos

optional arguments:
  -h, --help            show this help message and exit
  --debug               Display debugging information
  -u USER, --user USER  User (default : user logged by the config file)
```

### users_followed

```
python users_followed.py -h
pipenv run python users_followed.py -h
```

```
usage: users_followed.py [-h] [--debug] [-u USER]

Get the users followed by another user

optional arguments:
  -h, --help            show this help message and exit
  --debug               Display debugging information
  -u USER, --user USER  Users to search (separated by comma)
```
