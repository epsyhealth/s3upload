# Sample S3 upload with logging and monitoring 

## Dependencies
- poetry package manager (https://python-poetry.org/)
- AWS Credentials
- Sentry DSN


## Setup 

```
export AWS_DEFAULT_REGION=us-east-1
export AWS_ACCESS_KEY_ID=xxxxxx
export AWS_SECRET_ACCESS_KEY=yyyyy
export SENTRY_DSN="zzzz"
```


## Install dependencies

```
poetry install 
```

## Usage

```
poetry run python upload.py --assume-role="<role>" --bucket=<bucket> <file>
```
