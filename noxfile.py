"""Nox sessions for automation."""

import nox


@nox.session(python=["3.11", "3.12"])
def tests(session: nox.Session) -> None:
    """Run the test suite with pytest and coverage.

    Args:
        session: The Nox session object.
    """
    session.run("poetry", "install", "--with=test", external=True)
    session.run(
        "poetry",
        "run",
        "pytest",
        "--cov=panelyze",
        "--cov-report=term-missing",
        "--cov-report=html",
        "--cov-report=xml",
        *session.posargs,
        external=True,
    )


@nox.session(python="3.11")
def lint(session: nox.Session) -> None:
    """Run all linting checks.

    Args:
        session: The Nox session object.
    """
    session.run("poetry", "install", "--with=lint", external=True)
    session.run(
        "poetry", "run", "black", "--check", "src", "tests", "noxfile.py", external=True
    )
    session.run(
        "poetry",
        "run",
        "isort",
        "--check-only",
        "src",
        "tests",
        "noxfile.py",
        external=True,
    )
    session.run("poetry", "run", "flake8", "src", "tests", external=True)


@nox.session(python="3.11")
def black(session: nox.Session) -> None:
    """Format code with black.

    Args:
        session: The Nox session object.
    """
    session.run("poetry", "install", "--with=lint", external=True)
    session.run("poetry", "run", "black", "src", "tests", "noxfile.py", external=True)


@nox.session(python="3.11")
def isort(session: nox.Session) -> None:
    """Sort imports with isort.

    Args:
        session: The Nox session object.
    """
    session.run("poetry", "install", "--with=lint", external=True)
    session.run("poetry", "run", "isort", "src", "tests", "noxfile.py", external=True)


@nox.session(name="pre-commit", python="3.11")
def precommit(session: nox.Session) -> None:
    """Run pre-commit hooks on all files.

    Args:
        session: The Nox session object.
    """
    session.run("poetry", "install", "--with=dev", external=True)
    session.run(
        "poetry",
        "run",
        "pre-commit",
        "run",
        "--all-files",
        *session.posargs,
        external=True,
    )
