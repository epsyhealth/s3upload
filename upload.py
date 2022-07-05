import os
from os import getenv
from os.path import basename

import boto3
import click as click
import sentry_sdk
from botocore.exceptions import ClientError
from loguru import logger

if "SENTRY_DSN" in os.environ:
    sentry_sdk.init(
        dsn=getenv("SENTRY_DSN"),
        traces_sample_rate=1.0,
    )


@click.command()
@click.option("--assume-role", required=True)
@click.option("--bucket", required=True)
@click.argument("file", type=click.Path(exists=True))
def cli(assume_role: str, file: str, bucket: str) -> int:

    client = boto3.client("sts")

    credentials = None
    try:
        assumed_role_object = client.assume_role(
            RoleArn=assume_role,
            RoleSessionName="blc-calc",
        )

        credentials = assumed_role_object["Credentials"]
    except (ClientError, KeyError):
        logger.exception("Failed to obtain temporary credentials")
        return 1

    s3 = boto3.resource(
        "s3",
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"],
    )

    try:
        file_name = basename(file)
        logger.info(f"Uploading {file} to {bucket} with name {file_name}")
        s3.meta.client.upload_file(file, bucket, file_name)
    except ClientError:
        logger.exception("Failed to upload file")


if __name__ == "__main__":
    cli()
