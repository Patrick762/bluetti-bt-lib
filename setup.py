"""Setup for pypi package"""

import os
import codecs
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = os.getenv("LIB_VERSION") or "0.0.0"
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
        # Lower bounds only, no upper caps. When Home Assistant installs this
        # library (uv `pip install` at integration load), unpinned requirements
        # make the resolver query the HA wheels index (wheels.home-assistant.io)
        # for the "latest compatible" version of every dependency, even when an
        # acceptable one is already installed by HA core. An index incident
        # (e.g. HTTP 522) then breaks the install. bleak, bleak-retry-connector,
        # async-timeout and cryptography are shipped by HA core; floors aligned
        # with the versions it provides let the resolver satisfy them from the
        # already-installed packages without hitting the index. No upper bound:
        # a cap could conflict with the (newer) version HA has already installed
        # and break the install. Numbers below match HA core 2026.6.0.
        "async-timeout>=4.0.3",
        "bleak>=3.0.2",
        "bleak-retry-connector>=4.6.1",
        "cryptography>=48.0.0",
        # Not part of HA core: these get downloaded regardless, so keep only a
        # modest floor rather than over-constraining.
        "crcmod>=1.7",
        "pyasn1>=0.4.8",
    ],
    keywords=[],
    entry_points={
        "console_scripts": [
            "bluetti-scan = bluetti_bt_lib.scripts.bluetti_scan:start",
            "bluetti-detect = bluetti_bt_lib.scripts.bluetti_detect:start",
            "bluetti-read = bluetti_bt_lib.scripts.bluetti_read:start",
            "bluetti-readall = bluetti_bt_lib.scripts.bluetti_readall:start",
            "bluetti-write = bluetti_bt_lib.scripts.bluetti_write:start",
            "bluetti-parse = bluetti_bt_lib.scripts.bluetti_parse:start",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
)
