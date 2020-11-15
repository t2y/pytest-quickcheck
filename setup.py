from setuptools import setup

VERSION = "0.8.6"
REQUIRES = ["pytest>=4.0,<6.0.0"]

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
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
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
    long_description_content_type="text/x-rst",
    classifiers=CLASSIFIERS,
    keywords=["test", "pytest", "quickcheck"],
    author="Tetsuya Morimoto",
    author_email="tetsuya.morimoto@gmail.com",
    url="https://github.com/t2y/pytest-quickcheck",
    platforms=["linux", "osx", "unix", "win32"],
    packages=["pytest_quickcheck"],
    entry_points={"pytest11": ["quickcheck = pytest_quickcheck.plugin"]},
    install_requires=REQUIRES,
    tests_require=["tox", "pytest", "pytest-pycodestyle", "pytest-flakes"],
)
