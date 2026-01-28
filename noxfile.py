"""Nox sessions for automation."""

import nox


@nox.session(name="pre-commit", python="3.11")
def precommit(session: nox.Session) -> None:
    """Run pre-commit hooks on all files.

    Args:
        session: The Nox session object.
    """
    session.run(
        "poetry", "config", "virtualenvs.create", "false", "--local", external=True
    )
    session.run("poetry", "install", "--with=dev", external=True)
    session.run(
        "pre-commit",
        "run",
        "--all-files",
        *session.posargs,
    )


@nox.session(python=["3.11", "3.12", "3.13"])
def tests(session: nox.Session) -> None:
    """Run the test suite with pytest and coverage.

    Args:
        session: The Nox session object.
    """
    session.run(
        "poetry", "config", "virtualenvs.create", "false", "--local", external=True
    )
    session.run("poetry", "install", "--with=test", external=True)
    session.run(
        "pytest",
        "--cov=panl",
        "--cov-report=term-missing",
        "--cov-report=html",
        "--cov-report=xml",
        *session.posargs,
    )


@nox.session(python="3.11")
def safety(session: nox.Session) -> None:
    """Scan dependencies for vulnerabilities.

    Args:
        session: The Nox session object.
    """
    session.run(
        "poetry", "config", "virtualenvs.create", "false", "--local", external=True
    )
    session.run("poetry", "install", "--only=main,test", external=True)
    session.run("safety", "scan", "--full-report")


@nox.session(python="3.11")
def docs(session: nox.Session) -> None:
    """Build the documentation and run xdoctest.

    Args:
        session: The Nox session object.
    """
    session.run(
        "poetry", "config", "virtualenvs.create", "false", "--local", external=True
    )
    session.run("poetry", "install", "--with=docs", external=True)

    # Build documentation
    session.run("sphinx-build", "docs", "docs/_build")

    # Run doctests in documentation
    session.run("sphinx-build", "-b", "doctest", "docs", "docs/_build")

    # Run xdoctest on the source code
    session.run("xdoctest", "src/panl", "all")
