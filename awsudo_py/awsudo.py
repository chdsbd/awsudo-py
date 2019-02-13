#!/usr/bin/env python3
"""
Set AWS environment variables using profiles. This is useful for something like
Terraform, which has poor support for AWS MFA.
"""
import argparse
from pathlib import Path
from typing import List, Optional, Dict, cast, NoReturn, Tuple
import os
import sys

from botocore import credentials
from botocore.session import Session
import boto3

Environment = Dict[str, str]


def run_program(executable: str, args: List[str], env: Environment) -> NoReturn:
    """
    We exec the included variable
    """
    os.execlpe(executable, executable, *args, env)


def get_credentials(
    profile: str = "default", environment: Optional[Environment] = None
) -> Environment:
    """
    Use session cache so users don't need to use MFA while there are valid
    session tokens. This is the behavior of the AWSCLI and what we are trying to
    emulate.

    Modified with support for profiles from:
    https://github.com/boto/botocore/pull/1338/#issuecomment-368472031
    """
    # By default the cache path is ~/.aws/boto/cache
    cli_cache = (Path.home() / ".aws" / "cli" / "cache").absolute()

    # Construct botocore session with cache
    session = Session(profile=profile)
    session.get_component("credential_provider").get_provider(
        "assume-role"
    ).cache = credentials.JSONFileCache(cli_cache)

    # return credentials from session
    creds = boto3.Session(
        botocore_session=session, profile_name=profile
    ).get_credentials()

    return {
        "AWS_ACCESS_KEY_ID": creds.access_key,
        "AWS_SECRET_ACCESS_KEY": creds.secret_key,
        "AWS_SESSION_TOKEN": creds.token,
    }


def get_environment(credentials: Dict[str, str]) -> Environment:
    """Return environment updated with credentials"""
    environ = os.environ.copy()
    for key, value in credentials.items():
        if value is None:
            environ.pop(key, None)
        else:
            environ[key] = value
    return environ


def parse_args(args: List[str]) -> Tuple[str, str, List[str]]:
    parser = argparse.ArgumentParser(
        description="Set environment variables using profile"
    )
    parser.add_argument(
        "-p", "--profile", help="AWS Profile to assume", default="default"
    )
    parser.add_argument("executable", help="executable to run", metavar="PROG")
    parser.add_argument(
        "args", nargs=argparse.REMAINDER, help=argparse.SUPPRESS, metavar="ARG"
    )
    # print help on error
    if len(args) < 2:
        parser.print_help()
        parser.exit(2)
    parsed = parser.parse_args(args=args[1:])
    return (
        cast(str, parsed.executable),
        cast(str, parsed.profile),
        cast(List[str], parsed.args),
    )


def main() -> NoReturn:
    executable, profile, args = parse_args(sys.argv)
    credentials = get_credentials(profile)
    environment = get_environment(credentials)
    run_program(executable, args, env=environment)


if __name__ == "__main__":
    main()
