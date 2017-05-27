from setuptools import setup

VERSION = "0.8.3"
REQUIRES = ["pytest>=2.2"]

try:
    LONG_DESCRIPTION = "".join([
        open("README.rst").read(),
        open("CHANGELOG.rst").read(),
    ])
except:
    LONG_DESCRIPTION = ""

CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.2",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Topic :: Utilities",
    "Topic :: Software Development :: Testing",
    "Topic :: Software Development :: Libraries",
    "Topic :: Software Development :: Quality Assurance",
]

setup(
    name="pytest-quickcheck",
    version=VERSION,
    description="pytest plugin to generate random data inspired by QuickCheck",
    license="Apache License 2.0",
    long_description=LONG_DESCRIPTION,
    classifiers=CLASSIFIERS,
    keywords=["test", "pytest", "quickcheck"],
    author="Tetsuya Morimoto",
    author_email="tetsuya.morimoto@gmail.com",
    url="https://bitbucket.org/pytest-dev/pytest-quickcheck",
    platforms=["linux", "osx", "unix", "win32"],
    packages=["pytest_quickcheck"],
    entry_points={"pytest11": ["quickcheck = pytest_quickcheck.plugin"]},
    install_requires=REQUIRES,
    tests_require=["tox", "pytest", "pytest-pep8", "pytest-flakes"],
)
