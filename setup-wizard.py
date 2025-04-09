#!/usr/bin/env python

from pathlib import Path
import subprocess as sp
from InquirerPy import prompt
import yaml

# Write as .secrets
# # snakemake
# export SNAKEMAKE_STORAGE_S3_ACCESS_KEY=
# export SNAKEMAKE_STORAGE_S3_SECRET_KEY=

# # s5cmd
# export AWS_ACCESS_KEY=$SNAKEMAKE_STORAGE_S3_ACCESS_KEY
# export AWS_SECRET_ACCESS_KEY=$SNAKEMAKE_STORAGE_S3_SECRET_KEY


secrets_path = Path.home() / ".secrets"
profile_path = Path.home() / ".config" / "snakemake" / "default" / "config.yaml"


def get_default_secret(var):
    if secrets_path.exists():
        # Check if the variable is already set
        try:
            return {"default": sp.check_output(f"source ~/.secrets; echo ${var}", shell=True, executable="bash").decode().strip()}
        except sp.CalledProcessError:
            pass
    return {}

def get_default_from_profile(key):
    if profile_path.exists():
        with open(profile_path, "r") as f:
            profile = yaml.safe_load(f)
            if key in profile:
                return {"default": yaml.safe_load(f).get(key)}
    return {}


questions = [
    {
        'type': 'input',
        'name': 'S3-access-key',
        'message': 'Enter S3 access key',
    } | get_default_secret("SNAKEMAKE_STORAGE_S3_ACCESS_KEY"),
    {
        "type": "input",
        "name": "S3-secret-key",
        "message": "Enter S3 secret key",
    } | get_default_secret("SNAKEMAKE_STORAGE_S3_SECRET_KEY"),
    {
        "type": "input",
        "name": "S3-prefix",
        "message": "Enter S3 prefix (e.g. s3://yourbucket/)",
    } | get_default_from_profile("default-storage-prefix"),
    {
        "type": "input",
        "name": "kubernetes-namespace",
        "message": "Enter kubernetes namespace",
    } | get_default_from_profile("kubernetes-namespace"),
]

answer = prompt(questions)

if not answer["S3-prefix"].startswith("s3://"):
    raise ValueError("Error: given S3 prefix does not start with s3://")


with open(secrets_path, "w") as secrets:
    print(f"export SNAKEMAKE_STORAGE_S3_ACCESS_KEY={answer['S3-access-key']}", file=secrets)
    print(f"export SNAKEMAKE_STORAGE_S3_SECRET_KEY={answer['S3-secret-key']}", file=secrets)
    print("export AWS_ACCESS_KEY=$SNAKEMAKE_STORAGE_S3_ACCESS_KEY", file=secrets)
    print("export AWS_SECRET_ACCESS_KEY=$SNAKEMAKE_STORAGE_S3_SECRET_KEY", file=secrets)

with open(profile_path, "w") as profile:
    yaml.safe_dump({
        "executor": "kubernetes",
        "kubernetes-namespace": answer["kubernetes-namespace"],
        "default-storage-provider": "s3",
        "default-storage-prefix": answer["S3-prefix"],
        "software-deployment-method": "conda",
    }, profile)