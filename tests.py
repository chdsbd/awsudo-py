from awsudo_py.awsudo import parse_args


def test_parse_args() -> None:
    """
     Verify we can correctly parse the args to a program. We want --help to be
     passed to terraform, not our program.
    """
    args = ["awsudo", "--profile", "admin", "terraform", "state", "push", "--help"]
    executable, profile, args = parse_args(args)
    assert profile == "admin"
    assert executable == "terraform"
    assert args == ["state", "push", "--help"]
