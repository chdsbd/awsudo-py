# awsudo
> A sudo-like tool to configure AWS environment variables and call programs

This script is useful for programs like Terraform, which doesn't support MFA when assuming roles. 


## Installation
```sh
python3 -m pip install awsudo-py
```

## Usage
```console
$ awsudo -p administrator@staging terraform apply

$ awsudo -p administrator@staging env | grep AWS
AWS_ACCESS_KEY_ID=AKIAIXMBKCITA257EHIQ
AWS_SECRET_ACCESS_KEY=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
```

```
usage: awsudo [-h] [-p PROFILE] PROG [ARG [ARG ...]]

Set environment variables using profile

positional arguments:
  PROG                  executable to run
  ARG                   args to run with program

optional arguments:
  -h, --help            show this help message and exit
  -p PROFILE, --profile PROFILE
                        AWS Profile to assume
```

## Development
[Poetry][poetry] is necessary to install this project for development.
```sh
# install dependencies
make install

# linting
make typecheck
make fmt
# error on bad formatting
make fmt-check
make lint

# testing
make test
# runs fmt, typecheck, build
make all 

# building/publishing
make clean
make build
make publish
# build and install program directly
make install-program
make uninstall-program

# run program (we can't pass args to Make)
poetry run awsudo
```
[poetry]: https://github.com/sdispater/poetry

## Prior Art
There are a lot of similar programs to this one. I believe [makethunder/awsudo][0] and [electronicarts/awsudo][1] are the best alternatives. The only problems with [makethunder/awsudo][0] are that it isn't published on pypi and that it doesn't use the newest api for caching sessions. [electronicarts/awsudo][1] has all of the features, but it uses an internal session cache, instead of sharing with awscli. If you need SAML support though, the internal cache is a necessary compromise, so this package is great in that case.

project|awscli profiles|session caching|SAML|language|published
---|---|---|---|---|---
this project|yes|yes|no|python3.6|pypi
[makethunder/awsudo][0]|yes|yes*|no|python|github
[electronicarts/awsudo][1]|yes|yes⦿|yes|ruby|rubygems
[pmuller/awsudo][2]|yes|no|no|python2.7, python3.5|pypi
[ingenieux/awsudo][3]|no|no|no|golang|no
[meltwater/awsudo][4]|yes|yes|no|bash, node|npm, dockerhub

\*  supports session caching through older technique using awscli as a dependency

⦿ uses a daemon to cache sessions internally

[0]: https://github.com/makethunder/awsudo
[1]: https://github.com/electronicarts/awsudo
[2]: https://github.com/pmuller/awsudo
[3]: https://github.com/ingenieux/awsudo
[4]: https://github.com/meltwater/awsudo
