"""Setup for pypi package"""

import os
import codecs
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "0.0.7"
DESCRIPTION = "Bluetti BT"

# Setting up
setup(
    name="bluetti-bt-lib",
    version=VERSION,
    author="Patrick762",
    author_email="<pip-bluetti-bt-lib@hosting-rt.de>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/Patrick762/bluetti-bt-lib",
    packages=find_packages(),
    install_requires=[
        "async_timeout",
        "asyncio",
        "bleak",
        "crcmod",
        "cryptography",
        "logging",
        "pyasn1",
    ],
    keywords=[],
    entry_points={
        "console_scripts": [
            "bluetti = bluetti_bt_lib.scripts.bluetti:start",
            "bluetti-scan = bluetti_bt_lib.scripts.bluetti_scan:start",
            "bluetti-detect = bluetti_bt_lib.scripts.bluetti_detect:start",
            "bluetti-read = bluetti_bt_lib.scripts.bluetti_read:start",
            "bluetti-write = bluetti_bt_lib.scripts.bluetti_write:start",
        ],
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
)
