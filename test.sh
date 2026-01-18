#!/bin/sh

# Execute unittests of python library inside docker
sudo docker build --force-rm=true --progress=plain -t bluetti-bt-tests -f Dockerfile.test .


