# AWS
For testing AWS scripts

## About
This project is a demo, and uses boto3 to manage AWS EC2 instance snapshots.

## Configuring

shotty uses the configuration file created byt the AWS cli

`aws configure --pprofile shotty`

## Running

`pipenv run python shotty.py <command> --project=PROJECT> <command>
<subcommand>

*command is list, start, stop*
*project* is optional tag name


